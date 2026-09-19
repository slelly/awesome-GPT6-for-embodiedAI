# Public social-video downloader

`scripts/download_social_video.py` downloads only MP4 files that are attributable to the supplied original public post. Its verified support is X: either direct post-scoped public HTML (default), or the explicitly selected public SaveTwitter form after an independent original-post ownership check. A conservative Xiaohongshu direct-page adapter is present but **not end-to-end supported or verified**; no source from this catalogue may be claimed downloadable through it. It uses no account, cookie, API token, login flow, CAPTCHA bypass, or private endpoint.

## Usage

Run one post:

```bash
python3 scripts/download_social_video.py \
  --url 'https://x.com/JillJia6/status/2100275532378317038' \
  --output-dir downloads/social-video \
  --frame-seconds 1

# Optional X-only third-party public form. This sends only this public post URL
# to SaveTwitter, then accepts a result only if it matches the post-scoped X media.
python3 scripts/download_social_video.py \
  --url 'https://x.com/JillJia6/status/2100275532378317038' \
  --provider savetwitter --output-dir downloads/social-video
```

Run a UTF-8 batch file (one public original-post URL per line; blank lines and `#` comments are ignored):

```bash
python3 scripts/download_social_video.py --input social-posts.txt --output-dir downloads/social-video
```

The downloader accepts only `https://x.com/<account>/status/<id>` (including `www`/`mobile` aliases) and `https://www.xiaohongshu.com/explore/<id>` or `/discovery/item/<id>`. It rejects profile, search, non-HTTPS, signed-media, and unrelated URLs. It limits requests with `--rate-limit` (default one second), has a bounded `--retries` count (default two after the first request), and uses per-request timeouts. A fresh complete HTTP 200 can succeed without ETag/Last-Modified when its known length and MP4 signature validate. A local `.part` file, however, can resume only with a stable ETag or Last-Modified validator: the request sends it as `If-Range`, then requires a matching `206 Content-Range` start/interval/total, matching validator, and exact response byte count. An existing `.part` without a validator is discarded and restarted from byte zero without Range. Changed resources, malformed/non-terminal ranges, or a final local size different from the known total cannot produce a success record. A verified content SHA-256 is also de-duplicated across different input posts.

`ledger.jsonl` records the original public post URL, platform/parser, check time, local filename, bytes, SHA-256, content type, optional frame filename/time/hash, and explicit failure reason. The transient media delivery address is recorded only without its query string and is never a source citation. A response must carry an MP4 `ftyp` signature before it is retained. `--frame-seconds` invokes the existing `ffmpeg` to derive a JPEG cover after a successful video verification; if frame extraction fails, the video remains a successful ledger record, and a later `--frame-seconds` invocation can add a missing frame to an already verified local video.

## Public-flow checks (2026-09-19)

- X’s three existing original-post URLs (`JillJia6/status/2100275532378317038`, `MarioChan2002/status/2100091875403469014`, and `ludocomito/status/2097329417760440461`) each returned public HTML without a login redirect. Their own Tweet-media nodes exposed direct `video.twimg.com` MP4 candidates; the downloader selects the largest declared resolution only within that post-scoped set and verifies the downloaded MP4 signature.
- End-to-end X result: at `2026-09-19T03:12:33Z`, the original post `https://x.com/JillJia6/status/2100275532378317038` was parsed by `x_public_html` and yielded `JillJia6-status-2100275532378317038-ac0c60b111.mp4` (2,044,491 bytes, SHA-256 `4cc00832dac1292f5dc063bcfdabd8b810beef8e954bd927854cbfa784316e86`). Its response was `video/mp4`, passed the MP4 `ftyp` signature check, and `ffprobe` identified H.264 video (960×720, 38.314667 seconds) plus AAC audio. `ffmpeg` extracted `JillJia6-status-2100275532378317038-ac0c60b111-frame-1s.jpg` at 1.0 seconds (SHA-256 `9eb3ec851253c22ac9e257b647f66c1156bb31767109fb21c46148f5b4641351`). A repeat invocation and a duplicate line in a batch input both skipped the verified local file; an X profile URL was rejected before any network request.
- SaveTwitter probe: `https://savetwitter.net/zh-cn3` returned a public form. Submitting the same public X post to its documented `api/ajaxSearch` endpoint returned wrapped candidates; at `2026-09-19T03:22:05Z`, `--provider savetwitter` decoded a candidate only to compare it against the input post's own scoped X media node, then downloaded the identical verified MP4 and frame above. The wrapper's signed URL is not retained as a source.
- kukutool probe: `https://dy.kukutool.com/xiaohongshu` returned only `<script src="/_guard/auto.js"></script>` (39 bytes); the guard script is obfuscated anti-automation code and exposed no public form or endpoint. No challenge was solved or bypassed, so kukutool is not integrated. The public Xiaohongshu root separately redirected to `/login?redirectPath=...`, and the catalogue has no verified original note URL. The conservative direct adapter is therefore unverified; a supplied note redirecting to login stops with `login_required_or_guest_access_unavailable`.

Downloaded media and its runtime ledger are intentionally outside the repository’s catalogue data. Keep the original post URL and the ledger entry when using a derived frame as a cover; do not cite a signed/transient delivery URL as the long-term source.
