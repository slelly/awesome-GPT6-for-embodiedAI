# Changelog

## 0.2.28 — 2026-09-19

- Rechecked all 13 formerly estimated records against concrete source entry points. Twelve now use an exact repository-creation, version-release, paper-submission, or original-X-post timestamp with an explicit event meaning and evidence URL; Drone-Bench remains explicitly estimated because its official page exposes no recoverable dated publication, post, code, or changelog entry.

## 0.2.27 — 2026-09-19

- Unified all Gallery date badges as the same green `YYYY-MMDD` treatment. The retained date ledger still carries estimated status, basis, rule, and uncertainty; this release changes only the visible presentation.

## 0.2.26 — 2026-09-19

- Filled the Gallery date display for all 31 retained projects through a separate, auditable publication-date ledger: 18 retained exact dates and 13 explicitly marked estimates.
- Month-only records display the documented month midpoint; records without a recoverable date display the retained first-observation date with `≈`, source basis, rule, and uncertainty rather than a claimed publication date.

## 0.2.23 lightweight delivery revision — 2026-09-19

- Adds an explicit 14-file lightweight-package exclusion list and Chinese placement guide. The 13 uploaded MP4 originals and one uploaded JPEG keep their original filenames under `site/assets/social/`; their percent-encoded page paths, existing poster covers, and media interaction are retained. Packaging also excludes local downloader outputs and interpreter/test caches, and never deletes local media.
- Records the X13 Dual-ALOHA exact X status URL supplied by the user. The Gallery renders `Post / 原帖`; the source and Social-link ledgers explicitly distinguish this user-supplied URL from an independent content verification.
- Gives every retained video a local JPEG poster extracted from its first decoded frame at `00:00:00`. This includes re-extracted Social covers and newly bundled first frames for P01, P08, P10, and P12; video controls, lazy/on-demand loading, original video URLs, and original user filenames remain unchanged.
- Removes the Gallery detail dialog completely: no `View details / 查看详情` button, popup DOM, popup event path, popup style, or popup-only bilingual UI remains. Cards retain their concise summary, scene tags, direct links, posters, and video controls.

## 0.2.23 — 2026-09-19

- Adds the supplied Dual-ALOHA video and extracted poster while keeping its original-post URL explicitly unverified. Adds the supplied Dexterous Hand Rubik’s Cube image, and explicitly moves X07 to Social despite its retained demo-page link; the 31-entry partition is now 17 Projects / 14 Social.

## 0.2.22 — 2026-09-19

- Adds 12 user-supplied, title-matched Social videos under Pages-relative `site/assets/social/`, with one extracted one-second poster frame per video. Cards and details retain controls with `preload="none"`; original-post links and X13’s missing-media state are unchanged.

## 0.2.21 — 2026-09-19

- Replaces Social-tab account/search leads with 12 verified exact X original-post URLs, rendered consistently as `Post / 原帖` on cards and details. The remaining Dual-ALOHA lead has no visitor-facing substitute link; `docs/SOCIAL_LINKS.md` records its unresolved status and the project-to-post verification basis.

## 0.2.20 — 2026-09-19

- Restores complete-download compatibility when a server supplies no resumable validator: a full HTTP 200 with exact known length and MP4 signature succeeds. Only an existing unvalidated `.part` is discarded and restarted from byte zero without a Range request.

## 0.2.19 — 2026-09-19

- Makes partial-video completion fail closed: a resume now requires a stable ETag or Last-Modified validator, sends it with `If-Range`, verifies the matching `206 Content-Range` interval/total and received-byte count, and refuses finalization unless local size equals the known total. New offline cases cover missing validators, changed resources, truncation, and non-terminal partial ranges.

## 0.2.18 — 2026-09-19

- Binds every X MP4 candidate to the input post's own Tweet-media node before resolution, validates Range resume `Content-Range` offsets and resource validators before appending, and de-duplicates identical verified content across distinct source inputs. Optional frame errors now preserve a successful video ledger record, and existing verified videos can receive a later frame.
- Probes the two user-specified public services: SaveTwitter's public X form is available as an explicit `--provider savetwitter` option only after its candidate matches the original X post's scoped media; kukutool's Xiaohongshu page returned only an anti-automation guard, so it is not integrated or claimed supported. The direct Xiaohongshu adapter remains unverified because no original note was available.

## 0.2.17 — 2026-09-19

- Adds a credential-free, resumable public-post downloader for X and Xiaohongshu MP4 media, with bounded retries/rate limiting, MP4 verification, SHA-256 ledgering, explicit restriction failures, and optional `ffmpeg` cover-frame extraction. X is end-to-end verified on an existing original post; Xiaohongshu is implemented but remains unverified because its public root redirected to login and this catalogue contains no verified original note URL.

## 0.2.16 — 2026-09-19

- Makes name search language-independent by always indexing the source Chinese title and the complete English translation, so changing the display language never changes the matching ID set.

## 0.2.15 — 2026-09-19

- Adds source-bounded sim / real scene tags to every card and a compact, case-insensitive AND search over English/Chinese titles and tags. Search stays within the selected Projects/Social tab and survives tab and language changes.
- Adds the source-linked scene-tag ledger. No project, media record, direct link, or detail view was removed.

## 0.2.14 — 2026-09-18

- Adds a source-linked, all-31-item Astra relevance review with concrete study interfaces, missing-evidence boundaries, preliminary recommendations, and separately de-duplicated candidates; no card was removed, hidden, or added.
- Refines the visitor-facing bilingual detail association sentences to name each work's specific prospective research interface while retaining stated evidence limits.

## 0.2.13 — 2026-09-18

Adds parallel Projects and Social gallery tabs. Entries with an independent repository or project page—including a social-linked entry with that formal route—remain in Projects; profile/post-only leads appear only in Social. The 31-entry catalogue is therefore partitioned into 18 Projects and 13 Social entries. A bounded X10 cover probe found HTML but no verified direct video input; no frame was created.

## 0.2.12 — 2026-09-18

Replaces the uniform detail disclaimer and link-name resource line with project-specific English and Chinese detail copy. Each detail combines the documented capability with a concrete, qualified potential use—for example, shared-harness testing, scene reconstruction, or task-specific evaluation—without presenting a potential use as a completed deployment.

## 0.2.11 — 2026-09-18

Restores a verified `Post / 原帖` link for known direct X status URLs and an `Author profile / 作者主页` link when only an account is retained; the social-link ledger explicitly lists missing original posts. Detail views now present the documented capability, linked reusable resources, and clearly potential future Astra relevance. The detail-media fallback is hidden for loaded images and playable videos, and shown only for missing or failed media.

## 0.2.10 — 2026-09-18

Removes the duplicate English and Chinese project-summary overlay from card images and videos. Each card now has one summary in its text body; covers, directly linked images, videos, posters, controls, fallbacks, and detail-media interaction remain unchanged.

## 0.2.9 — 2026-09-18

Shows each project's de-duplicated Paper, Code, and Project page links directly on its card and in its detail view, always in that order. Only those three true target classes are rendered: GitHub repositories take Code precedence, while X, media, datasets, demos, author pages, search URLs, and image-source URLs remain in the source records but are not visitor-facing links.

## 0.2.8 — 2026-09-18

Classifies card and detail links by their URL target: GitHub repositories are `Code / 代码`, independent pages (including `github.io`) are `Project page / 项目主页`, and papers, demos, datasets, X announcements/profiles/searches retain their actual labels. Duplicate targets keep the first correctly classified label; Image source remains independent.

## 0.2.7 — 2026-09-18

Rewrites the rendered Gallery copy for visitors: project-focused header, summary, links, footer, and `Preview unavailable / 暂无预览` fallback. English/Chinese controls remain unchanged; project facts, source links, image provenance, media, and interactions are unchanged.

## 0.2.6 — 2026-09-18

Adds five directly loaded, source-linked project images for P13–P17 while retaining the prior seven images and four videos. Each new image records its source page, original repository path/branch or external-asset path, classification, and a concise detail-dialog “Image source” link. Every remaining missing-media entry now records its checked project/profile/search entrances and reason; method figures are explicitly not labelled as experiment demonstrations.

## 0.2.5 — 2026-09-18

Removes two Awesome-style collection cards (`P18`, `P19`) and eight anchor-only cards (`R01`–`R08`) whose normalized primary URL was the same Awesome Astra Embodied AI repository. The generated catalogue/CSV/page and both README entry counts now show the resulting 31 real project, resource, or X-lead entries. The retained 11 directly linked image/video records are unchanged.

## 0.2.4 — 2026-09-18

Adds an explicit 0.2.2 media-regression gate: all eleven retained direct media records must remain present in card and detail views, preserving seven image covers and four playable videos with their original URLs.

## 0.2.3 — 2026-09-18

Removes the top notice, search, reset toolbar, and their related runtime references. The Gallery now follows the title introduction directly; bilingual language switching, responsive layout, media fallback, and project detail views remain.

## 0.2.2 — 2026-09-18

Simplifies the Gallery presentation: cards no longer show evidence, environment, category, date, or source-state badges; only search remains. Detail views now contain the project name, demo, concise description/key results, and de-duplicated human-readable main links. Maintenance fields remain in the JSON catalogue.

## 0.2.1 — 2026-09-18

Fixes the Gallery JavaScript parse error and detail-media replacement lifecycle; implements first-supported-language selection, translated detail controls and metric headers, media-overlay summaries, keyboard/click detail opening, and video controls with `preload="none"`. Adds 8 further attributable primary-host media records (11 total), explicit missing-media reasoning, and a real Chromium interaction acceptance check.

## 0.2.0 — 2026-09-18

Reorganizes the source as a single repository root and makes English the default README with a prominent Chinese edition. Adds a bilingual, source-aware Gallery with saved language choice, browser-language fallback, evidence dialogs, attributable external media, explicit media-failure/missing fallbacks, and a generated media ledger. Extends validation, offline tests, Pages deployment gates, and local preview/publishing documentation.

No generated images, copied third-party media, remote repository, Pages deployment, or harvesting task was added.

## 0.1.0 — 2026-09-18

First public-ready source snapshot. Includes 41 tiered catalogue entries, 8 cross-linked Hugging Face resources, 51 source records and 34 representative search queries. Adds Chinese/English entry points, evidence and reproducibility documentation, a self-contained searchable website, validation scripts, tests, contribution templates and optional manual Pages deployment.

No remote repository was created; no third-party robot, simulator or paid model experiments were run. Social and secondary leads remain explicitly separated from primary project evidence.
