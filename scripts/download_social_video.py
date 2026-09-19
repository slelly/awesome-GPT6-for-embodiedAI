#!/usr/bin/env python3
"""Download publicly exposed video from an original X or Xiaohongshu post.

No cookies, credentials, private APIs, login automation, or anti-bot bypasses are
used.  The input must be a public original-post URL, not a profile, search page,
or a signed media URL.  Resolved delivery URLs are deliberately recorded only as
their origin/path (without query strings) because they are transient transports,
not source citations.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests


USER_AGENT = "awesome-GPT6-for-embodiedAI-social-video/0.1 (public, no-auth)"
X_HOSTS = {"x.com", "www.x.com", "mobile.x.com"}
XHS_HOSTS = {"xiaohongshu.com", "www.xiaohongshu.com"}
VIDEO_RE = re.compile(r"https?://[^\"'<>\\\s]+?\.mp4(?:\?[^\"'<>\\\s]*)?", re.I)


class DownloadFailure(RuntimeError):
    """A deliberate, user-readable stop for one source URL."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_source(url: str) -> tuple[str, str]:
    parsed = urlparse(url.strip())
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https":
        raise DownloadFailure("only_https_public_urls_are_allowed")
    if host in X_HOSTS:
        if not re.fullmatch(r"/[A-Za-z0-9_]+/status/\d+/?", parsed.path):
            raise DownloadFailure("x_requires_an_original_status_url")
        return "x", f"https://x.com{parsed.path.rstrip('/')}"
    if host in XHS_HOSTS:
        if not re.match(r"/(?:explore|discovery/item)/", parsed.path):
            raise DownloadFailure("xiaohongshu_requires_an_original_explore_or_item_url")
        return "xiaohongshu", f"https://www.xiaohongshu.com{parsed.path.rstrip('/')}"
    raise DownloadFailure("unsupported_site_expected_x_or_xiaohongshu")


def transient_origin(url: str) -> str:
    """Keep a reproducibility hint without retaining a potentially signed query."""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def request_with_retry(session: requests.Session, url: str, *, stream: bool, timeout: float, retries: int, headers: dict[str, str] | None = None) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            response = session.get(url, timeout=(timeout, timeout), allow_redirects=True, stream=stream, headers=headers)
            if response.status_code >= 500:
                response.close()
                raise DownloadFailure(f"http_{response.status_code}")
            return response
        except (requests.RequestException, DownloadFailure) as exc:
            last_error = exc
            if attempt == retries:
                break
            time.sleep(min(4.0, 0.8 * (2**attempt)))
    raise DownloadFailure(f"request_failed:{last_error}")


def post_with_retry(session: requests.Session, url: str, data: dict[str, str], *, timeout: float, retries: int, headers: dict[str, str]) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            response = session.post(url, data=data, timeout=(timeout, timeout), allow_redirects=True, headers=headers)
            if response.status_code >= 500:
                response.close()
                raise DownloadFailure(f"http_{response.status_code}")
            return response
        except (requests.RequestException, DownloadFailure) as exc:
            last_error = exc
            if attempt == retries:
                break
            time.sleep(min(4.0, 0.8 * (2**attempt)))
    raise DownloadFailure(f"post_failed:{last_error}")


def public_html(session: requests.Session, source: str, timeout: float, retries: int) -> tuple[str, str]:
    response = request_with_retry(session, source, stream=False, timeout=timeout, retries=retries)
    try:
        final = response.url
        if "/login" in urlparse(final).path:
            raise DownloadFailure("login_required_or_guest_access_unavailable")
        if response.status_code != 200:
            raise DownloadFailure(f"post_http_{response.status_code}")
        if "html" not in response.headers.get("content-type", "").lower():
            raise DownloadFailure("post_did_not_return_html")
        return response.text, final
    finally:
        response.close()


def mp4_candidates(page: str) -> list[str]:
    decoded = html.unescape(page).replace("\\u002F", "/").replace("\\/", "/")
    return list(dict.fromkeys(VIDEO_RE.findall(decoded)))


def pixel_area(url: str) -> int:
    match = re.search(r"/(\d+)x(\d+)/", url)
    return int(match.group(1)) * int(match.group(2)) if match else -1


def x_status_id(source: str) -> str:
    return urlparse(source).path.rstrip("/").split("/")[-1]


def x_post_mp4_candidates(page: str, source: str) -> list[str]:
    """Read variants owned by this Tweet node, never every MP4 in the page."""
    decoded = html.unescape(page).replace("\\u002F", "/").replace("\\/", "/")
    marker = base64.b64encode(f"Tweet:{x_status_id(source)}".encode()).decode()
    pattern = re.compile(
        rf'client:{re.escape(marker)}:media_entities(?:2)?:\d+:video_info:variants:\d+"[^}}]{{0,1400}}?'
        r'content_type:"video/mp4",url:"(https://video\.twimg\.com/[^"\\]+?\.mp4(?:\?[^"\\]*)?)"',
        re.I,
    )
    return list(dict.fromkeys(pattern.findall(decoded)))


def xiaohongshu_post_mp4_candidates(page: str, source: str) -> list[str]:
    """Conservatively require the original note ID near every retained URL."""
    decoded = html.unescape(page).replace("\\u002F", "/").replace("\\/", "/")
    note_id = urlparse(source).path.rstrip("/").split("/")[-1]
    candidates = []
    for match in VIDEO_RE.finditer(decoded):
        neighbourhood = decoded[max(0, match.start() - 1200):match.end() + 300]
        if note_id and note_id in neighbourhood:
            candidates.append(match.group(0))
    return list(dict.fromkeys(candidates))


def attributed_mp4_candidates(platform: str, page: str, source: str) -> list[str]:
    if platform == "x":
        return x_post_mp4_candidates(page, source)
    if platform == "xiaohongshu":
        return xiaohongshu_post_mp4_candidates(page, source)
    return []


def resolve_public_video(platform: str, page: str, source: str) -> str:
    candidates = attributed_mp4_candidates(platform, page, source)
    if not candidates:
        raise DownloadFailure(f"{platform}_post_exposed_no_attributable_public_mp4_candidate")
    # Resolution selection occurs only after ownership has been bound to the
    # input post. HLS manifests are intentionally not guessed.
    return max(candidates, key=pixel_area)


def decode_savetwitter_candidate(href: str) -> str | None:
    """Read the transient direct URL from SaveTwitter's signed wrapper locally."""
    token = parse_qs(urlparse(html.unescape(href)).query).get("token", [""])[0]
    parts = token.split(".")
    if len(parts) != 3:
        return None
    try:
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        value = json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
        return None
    url = value.get("url")
    return url if isinstance(url, str) else None


def savetwitter_confirmed_candidate(session: requests.Session, source: str, post_candidates: list[str], timeout: float, retries: int) -> str:
    """Use the public SaveTwitter form only if it resolves to this post's media."""
    response = post_with_retry(
        session,
        "https://savetwitter.net/api/ajaxSearch",
        {"q": source, "lang": "zh-cn3", "cftoken": ""},
        timeout=timeout,
        retries=retries,
        headers={"Referer": "https://savetwitter.net/zh-cn3", "Accept": "application/json", "X-Requested-With": "XMLHttpRequest"},
    )
    try:
        if response.status_code != 200:
            raise DownloadFailure(f"savetwitter_http_{response.status_code}")
        payload = response.json()
        if payload.get("status") != "ok" or not isinstance(payload.get("data"), str):
            raise DownloadFailure("savetwitter_did_not_return_download_candidates")
        wrapped = re.findall(r'href=["\']([^"\']+)', payload["data"], re.I)
        resolved = [candidate for href in wrapped if (candidate := decode_savetwitter_candidate(href))]
        attributed = [candidate for candidate in resolved if candidate in post_candidates]
        if not attributed:
            raise DownloadFailure("savetwitter_candidates_not_attributable_to_input_post")
        return max(attributed, key=pixel_area)
    finally:
        response.close()


def is_mp4_prefix(prefix: bytes) -> bool:
    return len(prefix) >= 12 and prefix[4:8] == b"ftyp"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def file_has_mp4_prefix(path: Path) -> bool:
    with path.open("rb") as handle:
        return is_mp4_prefix(handle.read(32))


def safe_name(source: str) -> str:
    parsed = urlparse(source)
    pieces = [piece for piece in parsed.path.split("/") if piece]
    stem = "-".join(pieces[-3:]) or "social-video"
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-")
    return f"{stem}-{hashlib.sha256(source.encode()).hexdigest()[:10]}.mp4"


def read_ledger(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def append_ledger(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def completed_record(records: list[dict], source: str, output_dir: Path) -> dict | None:
    for record in reversed(records):
        if record.get("source_url") != source or record.get("status") not in {"downloaded", "duplicate"}:
            continue
        file_path = output_dir / record.get("file", "")
        if file_path.is_file() and sha256_file(file_path) == record.get("sha256"):
            return record
    return None


def duplicate_content_record(records: list[dict], digest: str, output_dir: Path) -> dict | None:
    for record in reversed(records):
        if record.get("status") not in {"downloaded", "duplicate"} or record.get("sha256") != digest:
            continue
        file_path = output_dir / record.get("file", "")
        if file_path.is_file() and sha256_file(file_path) == digest:
            return record
    return None


def partial_meta_path(partial: Path) -> Path:
    return partial.with_name(partial.name + ".json")


def load_partial_meta(partial: Path) -> dict | None:
    try:
        return json.loads(partial_meta_path(partial).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def clear_partial(partial: Path) -> None:
    partial.unlink(missing_ok=True)
    partial_meta_path(partial).unlink(missing_ok=True)


def content_range(response: requests.Response) -> tuple[int, int, int | None] | None:
    value = response.headers.get("content-range", "")
    match = re.fullmatch(r"bytes\s+(\d+)-(\d+)/(\d+|\*)", value, re.I)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), None if match.group(3) == "*" else int(match.group(3))


def response_validator(response: requests.Response, media_url: str, total: int | None) -> dict:
    etag = response.headers.get("etag")
    last_modified = response.headers.get("last-modified")
    if_range = etag if etag and not etag.startswith("W/") else last_modified
    return {
        "media_origin": transient_origin(media_url),
        "etag": etag,
        "last_modified": last_modified,
        "if_range": if_range,
        "total": total,
    }


def resume_matches(offset: int, response: requests.Response, meta: dict | None, media_url: str) -> bool:
    span = content_range(response)
    if response.status_code != 206 or span is None or span[0] != offset or meta is None or not meta.get("if_range"):
        return False
    if meta.get("media_origin") != transient_origin(media_url):
        return False
    if meta["if_range"] == meta.get("etag"):
        if response.headers.get("etag") != meta["if_range"]:
            return False
    elif response.headers.get("last-modified") != meta["if_range"]:
        return False
    return (
        isinstance(meta.get("total"), int)
        and span[2] == meta["total"]
        and 0 <= span[0] <= span[1] < span[2]
        and offset < span[2]
    )


def declared_length(response: requests.Response) -> int | None:
    try:
        value = int(response.headers.get("content-length", ""))
    except ValueError:
        return None
    return value if value >= 0 else None


def download_mp4(session: requests.Session, url: str, target: Path, timeout: float, retries: int) -> tuple[str, int, str]:
    partial = target.with_suffix(target.suffix + ".part")
    last_error: Exception | None = None
    content_type = ""
    for attempt in range(retries + 1):
        offset = partial.stat().st_size if partial.exists() else 0
        meta = load_partial_meta(partial) if offset else None
        if offset and (not file_has_mp4_prefix(partial) or meta is None or not meta.get("if_range") or not isinstance(meta.get("total"), int)):
            clear_partial(partial)
            offset = 0
            meta = None
        if offset and meta and offset == meta["total"]:
            partial.replace(target)
            partial_meta_path(partial).unlink(missing_ok=True)
            return sha256_file(target), target.stat().st_size, "video/mp4"
        headers = {"Range": f"bytes={offset}-", "If-Range": meta["if_range"]} if offset and meta else None
        response: requests.Response | None = None
        try:
            # A stream can fail after response headers.  Retry the whole stream
            # with Range rather than treating an incomplete .part as success.
            response = request_with_retry(session, url, stream=True, timeout=timeout, retries=0, headers=headers)
            if response.status_code not in {200, 206}:
                raise DownloadFailure(f"media_http_{response.status_code}")
            if offset and response.status_code == 200:
                # If-Range deliberately caused a full response after a changed
                # resource or non-range server. Treat it as a verified restart.
                clear_partial(partial)
                offset, meta = 0, None
            elif offset and not resume_matches(offset, response, meta, url):
                # A server ignored Range, pointed us at a different object, or
                # gave a malformed/misaligned Content-Range: do not append.
                clear_partial(partial)
                continue
            if not offset and response.status_code != 200:
                clear_partial(partial)
                continue
            content_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
            expected = declared_length(response)
            if expected is None:
                raise DownloadFailure("media_missing_known_content_length")
            span = content_range(response)
            if offset:
                if span is None or expected != span[1] - span[0] + 1:
                    raise DownloadFailure("resume_content_length_does_not_match_content_range")
            elif span is not None:
                raise DownloadFailure("initial_response_unexpected_content_range")
            iterator = response.iter_content(chunk_size=1024 * 1024)
            first = next(iterator, b"")
            if not first or (not offset and not is_mp4_prefix(first[:32])):
                raise DownloadFailure(f"response_is_not_mp4:content_type={content_type or 'missing'}")
            if not offset:
                validator = response_validator(response, url, expected)
                partial_meta_path(partial).write_text(json.dumps(validator, sort_keys=True), encoding="utf-8")
            received = len(first)
            with partial.open("ab" if offset else "wb") as handle:
                handle.write(first)
                for chunk in iterator:
                    if chunk:
                        handle.write(chunk)
                        received += len(chunk)
            if received != expected:
                raise DownloadFailure(f"media_truncated_received_{received}_expected_{expected}")
            current_meta = load_partial_meta(partial)
            if not current_meta or partial.stat().st_size != current_meta.get("total"):
                raise DownloadFailure("media_final_length_does_not_match_known_total")
            break
        except (requests.RequestException, DownloadFailure) as exc:
            last_error = exc
            if attempt == retries:
                raise DownloadFailure(f"media_download_failed:{last_error}") from exc
            time.sleep(min(4.0, 0.8 * (2**attempt)))
        finally:
            if response is not None:
                response.close()
    meta = load_partial_meta(partial)
    if not partial.exists() or partial.stat().st_size < 12 or not meta or partial.stat().st_size != meta.get("total"):
        raise DownloadFailure("downloaded_file_failed_mp4_signature_check")
    if not file_has_mp4_prefix(partial):
        raise DownloadFailure("downloaded_file_failed_mp4_signature_check")
    partial.replace(target)
    partial_meta_path(partial).unlink(missing_ok=True)
    return sha256_file(target), target.stat().st_size, content_type


def extract_frame(video: Path, seconds: float) -> Path:
    frame = video.with_suffix("")
    frame = frame.with_name(frame.name + f"-frame-{seconds:g}s.jpg")
    command = ["ffmpeg", "-y", "-ss", str(seconds), "-i", str(video), "-frames:v", "1", "-q:v", "2", str(frame)]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=45)
    except FileNotFoundError as exc:
        raise DownloadFailure("ffmpeg_not_available_for_frame_extraction") from exc
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise DownloadFailure("ffmpeg_frame_extraction_failed") from exc
    if not frame.is_file() or frame.stat().st_size == 0:
        raise DownloadFailure("ffmpeg_produced_no_frame")
    return frame


def frame_result(record: dict, video: Path, seconds: float, extractor=extract_frame) -> dict:
    """Keep a verified download successful even if its optional frame fails."""
    result = dict(record)
    try:
        frame = extractor(video, seconds)
    except DownloadFailure as exc:
        result.update({"frame_status": "failed", "frame_seconds": seconds, "frame_failure_reason": str(exc)})
    else:
        result.update({"frame_status": "extracted", "frame_file": frame.name, "frame_seconds": seconds, "frame_sha256": sha256_file(frame)})
    return result


def has_verified_frame(records: list[dict], source: str, file_name: str, seconds: float, output_dir: Path) -> bool:
    for record in reversed(records):
        if record.get("source_url") != source or record.get("file") != file_name or record.get("frame_seconds") != seconds:
            continue
        frame = output_dir / record.get("frame_file", "")
        if record.get("frame_status", "extracted") == "extracted" and frame.is_file() and sha256_file(frame) == record.get("frame_sha256"):
            return True
    return False


def input_urls(args: argparse.Namespace) -> list[str]:
    values = list(args.url or [])
    if args.input:
        values.extend(line.strip() for line in Path(args.input).read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#"))
    if not values:
        raise SystemExit("provide --url or --input")
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", action="append", help="one public original X or Xiaohongshu post URL; may repeat")
    parser.add_argument("--input", help="UTF-8 file with one public original-post URL per line")
    parser.add_argument("--output-dir", default="downloads/social-video", help="destination and resumable ledger directory")
    parser.add_argument("--timeout", type=float, default=20.0, help="per-request connect/read timeout in seconds")
    parser.add_argument("--retries", type=int, default=2, help="finite retries after the first request")
    parser.add_argument("--rate-limit", type=float, default=1.0, help="minimum seconds between source posts")
    parser.add_argument("--frame-seconds", type=float, help="extract one verified JPEG cover frame with ffmpeg")
    parser.add_argument("--provider", choices=("direct", "savetwitter"), default="direct", help="direct original-post HTML (default), or the explicitly requested public SaveTwitter form for X")
    args = parser.parse_args()
    if args.timeout <= 0 or args.retries < 0 or args.rate_limit < 0 or (args.frame_seconds is not None and args.frame_seconds < 0):
        raise SystemExit("timeout must be positive; retries, rate-limit, and frame-seconds cannot be negative")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = output_dir / "ledger.jsonl"
    records = read_ledger(ledger_path)
    seen: set[str] = set()
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
    failures = 0

    for raw in input_urls(args):
        timestamp = utc_now()
        try:
            platform, source = canonical_source(raw)
            if source in seen:
                print(f"SKIP duplicate input {source}")
                continue
            seen.add(source)
            prior = completed_record(records, source, output_dir)
            if prior:
                if args.frame_seconds is not None and not has_verified_frame(records, source, prior["file"], args.frame_seconds, output_dir):
                    supplement = {"checked_at": timestamp, "source_url": source, "platform": platform, "parser_service": "existing_verified_video", "file": prior["file"], "sha256": prior["sha256"], "bytes": prior.get("bytes"), "content_type": prior.get("content_type"), "status": "downloaded"}
                    supplement = frame_result(supplement, output_dir / prior["file"], args.frame_seconds)
                    append_ledger(ledger_path, supplement)
                    records.append(supplement)
                    print(f"FRAME {source} -> {supplement.get('frame_status')}")
                else:
                    print(f"SKIP resumable existing {source} -> {prior['file']}")
                continue
            time.sleep(args.rate_limit)
            page, final_post = public_html(session, source, args.timeout, args.retries)
            post_candidates = attributed_mp4_candidates(platform, page, source)
            if not post_candidates:
                raise DownloadFailure(f"{platform}_post_exposed_no_attributable_public_mp4_candidate")
            if args.provider == "savetwitter":
                if platform != "x":
                    raise DownloadFailure("savetwitter_supports_x_only")
                media_url = savetwitter_confirmed_candidate(session, source, post_candidates, args.timeout, args.retries)
                parser_service = "savetwitter_public_ajax_confirmed_by_x_post_html"
            else:
                media_url = max(post_candidates, key=pixel_area)
                parser_service = f"{platform}_post_scoped_public_html"
            target = output_dir / safe_name(source)
            digest, byte_count, content_type = download_mp4(session, media_url, target, args.timeout, args.retries)
            duplicate = duplicate_content_record(records, digest, output_dir)
            if duplicate and duplicate.get("file") != target.name:
                target.unlink(missing_ok=True)
                record = {"checked_at": timestamp, "source_url": source, "platform": platform, "parser_service": parser_service, "post_final_url": final_post, "transient_download_origin": transient_origin(media_url), "file": duplicate["file"], "sha256": digest, "bytes": duplicate.get("bytes", byte_count), "content_type": duplicate.get("content_type", content_type), "status": "duplicate", "duplicate_of_source_url": duplicate.get("source_url")}
            else:
                record = {"checked_at": timestamp, "source_url": source, "platform": platform, "parser_service": parser_service, "post_final_url": final_post, "transient_download_origin": transient_origin(media_url), "file": target.name, "sha256": digest, "bytes": byte_count, "content_type": content_type, "status": "downloaded"}
            if args.frame_seconds is not None:
                record = frame_result(record, output_dir / record["file"], args.frame_seconds)
            append_ledger(ledger_path, record)
            records.append(record)
            print(f"{record['status'].upper()} {source} -> {record['file']} ({byte_count} bytes, sha256 {digest})")
        except (DownloadFailure, requests.RequestException) as exc:
            failures += 1
            source_value = raw.strip()
            try:
                _, source_value = canonical_source(raw)
            except DownloadFailure:
                pass
            record = {"checked_at": timestamp, "source_url": source_value, "parser_service": "input_validation_or_public_html", "status": "failed", "failure_reason": str(exc)}
            append_ledger(ledger_path, record)
            records.append(record)
            print(f"FAILED {source_value}: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
