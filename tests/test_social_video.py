"""Offline checks for the public social-video downloader safety contract."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import download_social_video as downloader  # noqa: E402


MP4 = b"\x00\x00\x00\x18ftypisom" + b"test-video-payload"


class FakeResponse:
    def __init__(self, status: int, headers: dict[str, str], chunks: list[bytes]):
        self.status_code = status
        self.headers = headers
        self._chunks = chunks
        self.closed = False

    def iter_content(self, chunk_size: int):
        yield from self._chunks

    def close(self):
        self.closed = True


class SocialVideoTests(unittest.TestCase):
    @staticmethod
    def resume_meta(url: str, total: int, etag: str | None = '"v1"') -> dict:
        return {"media_origin": downloader.transient_origin(url), "etag": etag, "last_modified": None, "if_range": etag, "total": total}

    def test_x_candidates_are_bound_to_input_post(self):
        source = "https://x.com/alice/status/12345"
        marker = downloader.base64.b64encode(b"Tweet:12345").decode()
        page = (
            "https://video.twimg.com/unrelated/vid/avc1/1920x1080/unrelated.mp4?tag=1 "
            f'client:{marker}:media_entities2:0:video_info:variants:1":$R={{'
            '__typename:"ApiMediaEntityVideoVariant",content_type:"video/mp4",'
            'url:"https://video.twimg.com/owned/vid/avc1/360x270/owned.mp4?tag=1"}}'
        )
        self.assertEqual(downloader.attributed_mp4_candidates("x", page, source), ["https://video.twimg.com/owned/vid/avc1/360x270/owned.mp4?tag=1"])

    def test_misaligned_range_is_discarded_before_full_restart(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "video.mp4"
            partial = target.with_suffix(".mp4.part")
            partial.write_bytes(MP4[:14])
            downloader.partial_meta_path(partial).write_text(json.dumps(self.resume_meta("https://video.example/video.mp4", len(MP4), '"old"')), encoding="utf-8")
            bad_resume = FakeResponse(206, {"content-range": f"bytes 0-{len(MP4) - 1}/{len(MP4)}", "etag": '"old"', "content-type": "video/mp4", "content-length": str(len(MP4))}, [MP4])
            fresh = FakeResponse(200, {"content-length": str(len(MP4)), "etag": "new", "content-type": "video/mp4"}, [MP4])
            with patch.object(downloader, "request_with_retry", side_effect=[bad_resume, fresh]):
                digest, size, content_type = downloader.download_mp4(object(), "https://video.example/video.mp4?signature=temporary", target, 1, 1)
            self.assertEqual(target.read_bytes(), MP4)
            self.assertEqual(digest, hashlib.sha256(MP4).hexdigest())
            self.assertEqual(size, len(MP4))
            self.assertEqual(content_type, "video/mp4")
            self.assertFalse(partial.exists())
            self.assertFalse(downloader.partial_meta_path(partial).exists())

    def test_complete_200_without_validator_succeeds(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "video.mp4"
            response = FakeResponse(200, {"content-type": "video/mp4", "content-length": str(len(MP4))}, [MP4])
            with patch.object(downloader, "request_with_retry", return_value=response):
                digest, size, content_type = downloader.download_mp4(object(), "https://video.example/video.mp4", target, 1, 0)
            self.assertEqual(target.read_bytes(), MP4)
            self.assertEqual(digest, hashlib.sha256(MP4).hexdigest())
            self.assertEqual(size, len(MP4))
            self.assertEqual(content_type, "video/mp4")

    def test_missing_validator_partial_is_discarded_then_restarted_without_range(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "video.mp4"
            partial = target.with_suffix(".mp4.part")
            partial.write_bytes(MP4[:14])
            downloader.partial_meta_path(partial).write_text(json.dumps({"media_origin": "https://video.example/video.mp4", "etag": None, "last_modified": None, "if_range": None, "total": len(MP4)}), encoding="utf-8")
            response = FakeResponse(200, {"content-type": "video/mp4", "content-length": str(len(MP4))}, [MP4])
            seen = []

            def request(*args, **kwargs):
                seen.append(kwargs.get("headers"))
                return response

            with patch.object(downloader, "request_with_retry", side_effect=request):
                downloader.download_mp4(object(), "https://video.example/video.mp4", target, 1, 0)
            self.assertEqual(seen, [None])
            self.assertEqual(target.read_bytes(), MP4)
            self.assertFalse(partial.exists())
            self.assertFalse(downloader.partial_meta_path(partial).exists())

    def test_changed_resource_range_is_not_appended_and_sends_if_range(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "video.mp4"
            partial = target.with_suffix(".mp4.part")
            partial.write_bytes(MP4[:14])
            url = "https://video.example/video.mp4"
            downloader.partial_meta_path(partial).write_text(json.dumps(self.resume_meta(url, len(MP4))), encoding="utf-8")
            changed = FakeResponse(206, {"content-range": f"bytes 14-{len(MP4) - 1}/{len(MP4)}", "content-length": str(len(MP4) - 14), "etag": '"v2"', "content-type": "video/mp4"}, [MP4[14:]])
            seen = []

            def request(*args, **kwargs):
                seen.append(kwargs.get("headers"))
                return changed

            with patch.object(downloader, "request_with_retry", side_effect=request):
                with self.assertRaises(downloader.DownloadFailure):
                    downloader.download_mp4(object(), url, target, 1, 0)
            self.assertEqual(seen[0], {"Range": "bytes=14-", "If-Range": '"v1"'})
            self.assertFalse(target.exists())

    def test_truncated_and_non_terminal_range_cannot_become_success(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            short_target = root / "short.mp4"
            short = FakeResponse(200, {"content-type": "video/mp4", "content-length": str(len(MP4)), "etag": '"v1"'}, [MP4[:-1]])
            with patch.object(downloader, "request_with_retry", return_value=short):
                with self.assertRaises(downloader.DownloadFailure):
                    downloader.download_mp4(object(), "https://video.example/short.mp4", short_target, 1, 0)
            self.assertFalse(short_target.exists())

            target = root / "range.mp4"
            partial = target.with_suffix(".mp4.part")
            partial.write_bytes(MP4[:14])
            url = "https://video.example/range.mp4"
            downloader.partial_meta_path(partial).write_text(json.dumps(self.resume_meta(url, len(MP4))), encoding="utf-8")
            non_terminal = FakeResponse(206, {"content-range": f"bytes 14-18/{len(MP4)}", "content-length": "5", "etag": '"v1"', "content-type": "video/mp4"}, [b"12345"])
            with patch.object(downloader, "request_with_retry", return_value=non_terminal):
                with self.assertRaises(downloader.DownloadFailure):
                    downloader.download_mp4(object(), url, target, 1, 0)
            self.assertFalse(target.exists())

    def test_cross_input_hash_dedup_uses_verified_existing_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            file_path = root / "first.mp4"
            file_path.write_bytes(MP4)
            digest = hashlib.sha256(MP4).hexdigest()
            records = [{"source_url": "https://x.com/a/status/1", "status": "downloaded", "file": "first.mp4", "sha256": digest}]
            duplicate = downloader.duplicate_content_record(records, digest, root)
            self.assertEqual(duplicate["source_url"], "https://x.com/a/status/1")
            self.assertIsNotNone(downloader.completed_record([{**duplicate, "source_url": "https://x.com/b/status/2", "status": "duplicate"}], "https://x.com/b/status/2", root))

    def test_frame_failure_does_not_change_download_success(self):
        with tempfile.TemporaryDirectory() as temporary:
            video = Path(temporary) / "video.mp4"
            video.write_bytes(MP4)
            record = {"status": "downloaded", "file": "video.mp4", "sha256": hashlib.sha256(MP4).hexdigest()}
            result = downloader.frame_result(record, video, 1.0, extractor=lambda *_: (_ for _ in ()).throw(downloader.DownloadFailure("ffmpeg_frame_extraction_failed")))
            self.assertEqual(result["status"], "downloaded")
            self.assertEqual(result["frame_status"], "failed")
            self.assertEqual(result["frame_failure_reason"], "ffmpeg_frame_extraction_failed")

    def test_existing_verified_video_can_receive_a_later_frame(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            video = root / "video.mp4"
            video.write_bytes(MP4)
            record = {"source_url": "https://x.com/a/status/1", "status": "downloaded", "file": "video.mp4", "sha256": hashlib.sha256(MP4).hexdigest()}
            self.assertFalse(downloader.has_verified_frame([record], record["source_url"], "video.mp4", 1.0, root))

            def extractor(path: Path, seconds: float) -> Path:
                frame = path.with_name("video-frame-1s.jpg")
                frame.write_bytes(b"jpeg")
                return frame

            framed = downloader.frame_result(record, video, 1.0, extractor=extractor)
            self.assertEqual(framed["status"], "downloaded")
            self.assertTrue(downloader.has_verified_frame([record, framed], record["source_url"], "video.mp4", 1.0, root))


if __name__ == "__main__":
    unittest.main()
