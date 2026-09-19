#!/usr/bin/env python3
"""Report decoded video metadata and compare frames across each retained clip.

The report is deliberately advisory: a clip is considered static only when
three decoded time samples match exactly.  Failed remote probes are reported
as errors rather than silently classified as still images.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, timeout=75, check=False)


def frame_digest(source: str, moment: float) -> str:
    result = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{moment:.3f}', '-i', source, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, timeout=75, check=False)
    if result.returncode or not result.stdout:
        raise RuntimeError(result.stderr.decode('utf-8', errors='replace').strip() or 'ffmpeg produced no frame')
    return hashlib.sha256(result.stdout).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    media = json.loads((ROOT / 'data' / 'media.json').read_text(encoding='utf-8'))['media']
    report: list[dict[str, object]] = []
    for project_id, item in media.items():
        if item.get('kind') != 'video':
            continue
        url = item['url']
        source = str((ROOT / 'site' / unquote(url)).resolve()) if not url.startswith(('http://', 'https://')) else url
        entry: dict[str, object] = {'id': project_id, 'source': url}
        try:
            probe = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=nb_frames,duration,width,height,avg_frame_rate', '-of', 'json', source])
            if probe.returncode:
                raise RuntimeError(probe.stderr.strip() or 'ffprobe failed')
            stream = json.loads(probe.stdout)['streams'][0]
            duration = float(stream.get('duration') or 0)
            moments = [0.0, duration * 0.5, max(0.0, duration * 0.9)]
            digests = [frame_digest(source, moment) for moment in moments]
            entry.update({'probe': stream, 'sample_seconds': [round(moment, 3) for moment in moments], 'sample_sha256': digests, 'motion': 'static' if len(set(digests)) == 1 else 'motion'})
        except (IndexError, KeyError, ValueError, subprocess.TimeoutExpired, RuntimeError) as error:
            entry.update({'motion': 'unverified', 'error': str(error)})
        report.append(entry)
    payload = {'method': 'ffprobe video-stream metadata plus SHA-256 of decoded PNG frames at 0%, 50%, and 90% duration', 'videos': report}
    text = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    else:
        print(text, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
