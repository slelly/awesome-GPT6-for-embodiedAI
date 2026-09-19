# Validation record

This record covers the catalogue source itself, not linked third-party robot systems.

## Passed locally

- `python3 scripts/validate.py`: 31 projects, 51 sources, 8 Hugging Face resources; schema, provenance, dates, URL syntax, normalized GitHub repository URL de-duplication, local Markdown links, complete English Gallery translation coverage, and media provenance checks pass.
- `python3 scripts/build.py`: deterministically generates the catalogue, source ledger, HF document, media ledger, CSV, and self-contained gallery page. Thirty media records are retained (seventeen videos and thirteen images), including thirteen user-supplied Social MP4s with extracted 1.0-second poster frames and one supplied X07 image under `site/assets/social/`. X13 has media and an exact X status URL supplied by the user; this record does not claim an independent content verification.
- `python3 -m unittest discover -s tests -v`: 30 tests pass and one historical 0.1.0 snapshot-count fixture is intentionally skipped after the 0.2.21 catalogue revision. The suite also checks that the Social tab has 13 distinct exact status targets, with X13 explicitly recorded as user-supplied rather than independently verified. The nine downloader tests prove post-scoped X candidate selection, cross-input verified-hash de-duplication, frame-failure record retention/later frame attachment, malformed-range restart, changed-resource rejection, refusal to finalize truncated/non-terminal ranges, successful complete 200 downloads without validators, and validator-free partial reset without Range.
- `python3 -m py_compile scripts/download_social_video.py`: passed. Direct X and explicit `--provider savetwitter` public runs each downloaded and signature-verified the 2,044,491-byte `JillJia6/status/2100275532378317038` MP4 (SHA-256 `4cc00832dac1292f5dc063bcfdabd8b810beef8e954bd927854cbfa784316e86`), then generated a 1.0-second JPEG frame. The complete source/frame/time/hash record and two-site probe outcomes are in `docs/SOCIAL_VIDEO_DOWNLOADER.md`; gallery media data remains unchanged.
- The running HTTPS preview returned HTTP 200 for the generated gallery and HTTP 404 for `/README.md`, confirming that its server root is `site/` rather than the repository root.

## Real-browser acceptance

`PYTHONPATH=../.preview/playwright python3 scripts/browser_check.py --browser /root/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome --screenshots ../.preview/screenshots-v27 --skip-screenshots` previously passed on 2026-09-19 for the non-overlapping 17 Projects / 14 Social partition, all 31 cards, X07’s supplied relative image, all thirteen relative Social MP4/poster pairs including X13, card/detail media controls and fallback behavior, English/Chinese links and search, mobile layout, and a Pages-style project subpath. The later X13 link addition is checked separately for its English and Chinese `Post / 原帖` card/detail rendering; it is a user-supplied exact URL rather than an independent content verification.

A focused real-Chromium check passed after the X13 update: both the Social card and detail dialog expose exactly `Post` in English and `原帖` in Chinese, each targeting `https://x.com/qineng_wang/status/2099893504658866561`; no page errors occurred. This checks rendering only and does not open or independently content-verify the external post.

## Video first-frame posters

All 17 retained videos now have a local JPEG poster referenced by the same media record in the card and detail dialog. The 13 supplied Social MP4 posters were re-extracted from the first decoded frame at `00:00:00`, replacing the earlier one-second frames. The four previously posterless external videos—P01 (GPT-Policy), P08 (GPT6-real2sim), P10 (Real2Gym), and P12 (Drone-Bench)—were reachable at their existing MP4 URLs and each yielded a first decoded frame at `00:00:00`; the small JPEGs are bundled under `site/assets/posters/`. No unrelated substitute image was used and no external video was unavailable in this run.

Real Chromium passed with all 17 poster URLs fetchable before playback, the matching `poster` attribute present in both card and detail video elements, `controls` retained, `preload="none"` retained, a card-video control click not opening the detail dialog, the Pages-style project subpath, and the mobile layout. The source file/path and `00:00:00` timestamp for every poster are recorded in `data/media.json` and the generated [media ledger](MEDIA.md). Local `ffprobe` also parses every supplied MP4 and every bundled poster JPEG.

## Detail UI removal

The Gallery no longer creates a detail dialog or any card/image/keyboard route to one. The current Chromium check verifies that both languages contain no detail button, dialog DOM, dialog styles, or dialog trigger; summaries, scene tags, direct links, 17 static posters, video controls, search, group switching, mobile layout, and the Pages-style subpath remain available. The focused current check passed with no page errors.

`ffprobe` decoded the X13 H.264 video (1280×720, 44.95 seconds), and `ffmpeg` extracted its one-second JPEG poster. The supplied X07 JPEG parses as a 1200×691 MJPEG image. The previous twelve MP4/frame checks remain valid.

`ffprobe` decoded the video stream of each of X01–X06, X08–X12 and X14 (all H.264, 5.0–303.7 seconds) and `ffmpeg` extracted the packaged one-second JPEG poster frames. This is an asset-integrity check; the browser check covers the published controls, relative URLs, posters, interaction and responsive layout.

## Lightweight delivery-package check

`scripts/package_lightweight.py` creates a ZIP with an explicit 14-file uploaded-media exclusion list: the thirteen newly uploaded MP4 originals and `SaveTwitter.Net_HST8HsrawAAkgPu.jpg`. It also excludes the local `downloads/` downloader outputs and interpreter/test caches; neither is a Gallery source asset. It does not delete local files; all extracted `X01.jpg`–`X14.jpg` poster covers (where applicable) and existing page media remain in the ZIP. The Chinese [placement guide](SOCIAL_MEDIA_PLACEMENT.zh-CN.md) gives the exact original filenames, including the two spaces in `Office Scene to Newton  G1.mp4`.

The delivered ZIP was tested with `unzip -t`; its member list contains none of those 14 originals and retains all 13 Social poster covers. In a fresh extraction, all 14 originals were copied back under `site/assets/social/` without renaming. Chromium then passed the full card/detail/media/control, English/Chinese/search, mobile, and Pages-style project-subpath checks against that extracted copy. The data URLs percent-encode spaces while resolving to the original filenames.

Chromium's screenshot capture remains a host-level limitation: both Playwright/CDP capture and Chrome's headless screenshot path stalled after page rendering, including a minimal `data:` page; the browser test was stopped after 15 seconds and produced no image. This is distinct from page loading and interaction, which pass. No generated image or non-browser substitute is included as a screenshot.

For the prior bounded X10 cover attempt, the known original-post URL returned HTML but no verified direct video input. The later public-post downloader is independently verified only on P03’s known X original post; it does not alter X10’s missing-media state. Xiaohongshu’s public root redirected to login in this environment, and no verified original Xiaohongshu note URL is present in the catalogue, so its adapter is documented as unverified. No login, endpoint-discovery workaround, or additional installation was attempted; existing gallery media/fallbacks remain unchanged.

## Not run

No third-party source checkout, model/data download, simulator run, robot experiment, GitHub repository creation, Pages deployment, or automated harvesting was run. The only new external media action was the one documented public X MP4 download above.
