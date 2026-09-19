#!/usr/bin/env python3
"""Create the lightweight delivery ZIP without deleting local media.

The media exclusion list is deliberately explicit: it contains only the 13
newly supplied MP4 files and one newly supplied JPEG. Their extracted poster
frames and every page-published Gallery asset remain in the archive. Local
downloader outputs and interpreter caches are excluded as runtime artifacts.
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA_DIR = Path('site/assets/social')
EXCLUDED_MEDIA = (
    'Physical Robot Keyboard Typing.mp4',
    'Physical Ethernet Insertion.mp4',
    'Robot Arm Draws the Golden Gate Bridge.mp4',
    'Cross-Scene Mobile Manipulation ICL.mp4',
    'G1 Coke-Bottle Grasp.mp4',
    'G1 Navigation.mp4',
    'Sharpa Dexterous-Hand Pen Spinning PPO.mp4',
    'Go1 Paused-Physics Joint Control.mp4',
    'CARLA Visual Waypoint Driving.mp4',
    'Two-Robot Ball Toss.mp4',
    'G1 Bicycle-Control Code.mp4',
    'Office Scene to Newton  G1.mp4',
    'Dual-ALOHA Spatial-Constraint Demo.mp4',
    'SaveTwitter.Net_HST8HsrawAAkgPu.jpg',
)
EXCLUDED_PATHS = {MEDIA_DIR / name for name in EXCLUDED_MEDIA}
RUNTIME_TOP_LEVEL = {'downloads', '.pytest_cache'}
RUNTIME_DIR_NAMES = {'__pycache__'}


def is_runtime_artifact(relative: Path) -> bool:
    """Runtime output is never part of the source/Gallery delivery package."""
    return relative.parts[0] in RUNTIME_TOP_LEVEL or bool(set(relative.parts) & RUNTIME_DIR_NAMES)


def package(output: Path) -> list[Path]:
    missing = [path for path in EXCLUDED_PATHS if not (ROOT / path).is_file()]
    if missing:
        raise ValueError(f'cannot make a verified lightweight package; missing originals: {missing}')
    output.parent.mkdir(parents=True, exist_ok=True)
    members: list[Path] = []
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(ROOT.rglob('*')):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT)
            if relative in EXCLUDED_PATHS or is_runtime_artifact(relative):
                continue
            archive.write(path, Path(ROOT.name) / relative)
            members.append(relative)
    with zipfile.ZipFile(output) as archive:
        actual = {Path(name).relative_to(ROOT.name) for name in archive.namelist() if not name.endswith('/')}
    leaked = EXCLUDED_PATHS & actual
    if leaked:
        raise ValueError(f'lightweight package contains excluded originals: {sorted(map(str, leaked))}')
    return members


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='destination ZIP, normally outside the repository root')
    parser.add_argument('--print-exclusions', action='store_true')
    args = parser.parse_args()
    if args.print_exclusions:
        print('\n'.join(str(path) for path in sorted(EXCLUDED_PATHS)))
        return 0
    members = package(args.output.resolve())
    print(f'created {args.output.resolve()} with {len(members)} files; excluded {len(EXCLUDED_PATHS)} uploaded originals plus runtime artifacts')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
