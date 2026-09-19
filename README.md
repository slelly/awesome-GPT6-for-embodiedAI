# Awesome GPT6 Embodied AI [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

An evidence-aware catalogue of GPT-6 Astra robotics, embodied evaluation, simulation engineering, and community demonstrations.

[中文版本 / Chinese](README.zh-CN.md) · [Gallery](site/index.html) · [Full catalogue](docs/CATALOG.md) · [Sources](docs/SOURCES.md) · [Scene tags](docs/SCENE_TAGS.md) · [Astra relevance review](docs/ASTRA_RELEVANCE_REVIEW.md) · [Media ledger](docs/MEDIA.md) · [Public social-video downloader](docs/SOCIAL_VIDEO_DOWNLOADER.md) · [Hugging Face](docs/HUGGING_FACE.md)

**Window:** August 18–September 18, 2026. **Snapshot:** September 18, 2026, Asia/Taipei. This is an independent curated snapshot, not an OpenAI resource, continuous monitoring service, or claim of exhaustive platform coverage. No robot/model experiments were independently run for this catalogue.

## Contents

- [Scope](#scope)
- [Gallery](#gallery)
- [Selected primary resources](#selected-primary-resources)
- [Key distinctions](#key-distinctions)
- [Use locally](#use-locally)
- [Publication and Awesome-list readiness](#publication-and-awesome-list-readiness)
- [Attribution and licensing](#attribution-and-licensing)

## Scope

31 entries: **12 directly relevant projects/evaluations**, **5 supporting resources**, and **14 X leads**. Two Awesome-style discovery collections and eight anchor-only duplicates from the same collection are retained as provenance credits, not presented as independent project cards. The 8 HF resources cross-reference projects and are not additional experiments. Several foundational resources predate the window; unknown dates and incomplete model attribution remain explicitly marked.

Evidence levels describe sources, not performance: **A** readable primary material; **B** primary entry with incomplete implementation or GPT-6-specific evidence; **C** readable mirror of an author's demonstration; **D** secondary discovery lead. A does not imply complete public code or successful reproduction.

## Gallery

`site/index.html` is a bilingual gallery. Its language order is an explicit saved choice, then the first supported browser language, then English. Each card opens a concise project description, key results where available, and de-duplicated main links. Media is only shown when this catalogue retained a directly linkable, attributable public image or video; entries without such media show an explicit fallback and keep the original project or lead URL. See the generated [media ledger](docs/MEDIA.md) for item-by-item provenance and omissions. Lightweight delivery packages omit only the large user-uploaded Social originals; the [Chinese placement guide](docs/SOCIAL_MEDIA_PLACEMENT.zh-CN.md) lists the exact filenames and destination.

## Selected primary resources

| Resource | Role | Important boundary |
| --- | --- | --- |
| [GPT-Policy](https://github.com/cheng-haha/GPT-Policy) | Real-robot in-context learning with constrained tools | License pending; not all experimental assets public |
| [GPT-as-Policy](https://github.com/anonymous-report-421/GPT-as-Policy) | Direct GPT vs π0.5 proposals reviewed/corrected by GPT | Selected aligned cases, not same-seed reruns of official baselines |
| [Agent as Policy](https://agent-as-policy-2026.github.io/) | Real-robot agent execution and feedback | Public trial data does not establish code availability |
| [RoboCurve](https://openai.robocurve.org/gpt-6-astra/) | Repeated real-robot bowl/puzzle trials | Task-dependent performance and protocol limitations |
| [StationeryBench](https://openai.robocurve.org/stationerybench/) | Five bimanual stationery tasks | Progress score is not full-completion rate |
| [GPT6-real2sim](https://github.com/lingxiao-guo/GPT6-real2sim) | MuJoCo/Blender reconstruction | Contact simulation, fitted trajectories and replay are distinct |
| [Real2Sim_GPT6_ASTRA](https://github.com/hku-sail/Real2Sim_GPT6_ASTRA) | Multi-view visual scene/action reconstruction | Editable animation is not validated physical control |

The full catalogue also includes ENPIRE, RoboDojo, Real2Gym, dexgpt, Drone-Bench, Inspect Robots, Show-Harness, PhysBrain, HumanCLAW and social discovery leads. **GPT-Policy, GPT-as-Policy and Agent as Policy are different projects.**

## Key distinctions

Record whether GPT-6 runs online, proposes tool actions, reviews another policy, writes code offline, optimizes RL training, or constructs a scene. Do not equate simulated control frequency with wall-clock inference frequency. Do not merge curated demonstrations, repeated trials, progress scores, VQA-style understanding benchmarks, and control success into one leaderboard.

Most X leads were read through search indexes or author-post mirrors. Unknown original tweet IDs are never synthesized. Original Rednote notes could not be verified; these remain secondary leads. Source access mode and date are retained for each record.

## Use locally

Open `site/index.html` directly or serve only the `site/` directory. It embeds the catalogue and uses no external scripts or API keys; the few attributable gallery images are loaded from their original public hosts and gracefully fall back if unavailable.

```bash
python scripts/validate.py
python scripts/build.py
python -m unittest discover -s tests -v
```

Core catalogue tooling uses Python 3.10+ standard library only. The optional [public social-video downloader](docs/SOCIAL_VIDEO_DOWNLOADER.md) uses the already-installed `requests` package and optional local `ffmpeg`; it does not use credentials or browser-login automation. Edit `data/projects.json`, `data/sources.json`, `data/i18n.json`, and `data/media.json`, then rebuild. Default CI and the Pages workflow perform offline validation, gallery-data checks, builds, tests, and generated-file checks; they do not run third-party robot experiments. See [publishing](docs/PUBLISHING.md), [methodology](docs/METHODOLOGY.md), and [reproducibility](docs/REPRODUCIBILITY.md).

## Publication and Awesome-list readiness

This repository is intentionally local until maintainers approve a public remote. The Pages workflow remains manual. When publishing, use a lowercase repository slug (for example, `awesome-gpt6-embodied`), set `awesome` and `awesome-list` topics, and confirm the current [Awesome list guidance](https://github.com/sindresorhus/awesome/blob/main/awesome.md): curate rather than aggregate, keep a succinct scope, use consistent entry descriptions, retain contribution guidance, and select a Creative Commons license if submitting to the upstream Awesome list. This local source bundle currently retains MIT for its original code and prose, so it must **not** be represented as eligible for upstream inclusion until maintainers decide on that license change.

## Attribution and licensing

Discovery credits: [Awesome Astra Embodied AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI) and [Awesome Robot Use Agent](https://github.com/kairunwen/Awesome-Robot-Use-Agent). Their entries are leads, not independent replications.

MIT applies only to this repository's original curation and tooling. Linked code, model weights, datasets, papers and media keep their respective terms. No third-party repository, font, robot asset, model weight or video is bundled. No remote GitHub repository has been published as part of this snapshot.
