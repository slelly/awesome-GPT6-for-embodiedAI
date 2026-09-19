# Awesome GPT6 Embodied AI [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

An evidence-aware, bilingual collection of GPT-6 Astra embodied-AI projects, evaluations, workflow resources, and attributable community demonstrations.

[中文版本 / Chinese](README.zh-CN.md) · [Gallery](site/index.html) · [Sources](docs/SOURCES.md) · [Media](docs/MEDIA.md) · [Tags](docs/TAGS.md) · [Date ledger](docs/PUBLICATION_DATES.md) · [Contributing](CONTRIBUTING.md)

## Contents

- [What is included](#what-is-included)
- [Browse by workflow tags](#browse-by-workflow-tags)
- [Dates and source credit](#dates-and-source-credit)
- [Use and GitHub Pages](#use-and-github-pages)
- [Attribution and license](#attribution-and-license)

## What is included

This snapshot contains 31 entries: 17 Projects and 14 Social posts. Projects and posts are grouped in the Gallery and sorted newest-first within their group, while every card keeps direct Paper, Code, Project page, or Post links where those targets exist.

The collection is organized around visitor-facing workflows, following the useful structure of [Awesome Astra Embodied AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI): clear source credit, a visible date, and workflow-oriented discovery. Unlike that reference list, this repository retains a per-entry evidence ledger and distinguishes direct projects from supporting resources and social leads.

## Browse by workflow tags

Cards combine factual scene tags with one or more workflow tags. Search accepts an English or Chinese project name, a tag, or multiple terms; multiple terms use AND matching.

| Scene | Workflow examples |
| --- | --- |
| `simulation` / `仿真` | `control`, `real-to-sim`, `replay`, `RL training`, `physics simulation` |
| `real world` / `真机` | `control`, `evaluation`, `policy`, `harness` |
| Cross-cutting | `benchmark`, `code generation`, `dexterous manipulation`, `environment building` |

Tags describe the work shown by the retained project material. They are not a claim that projects share a benchmark, deployment setting, or model result. The complete tag vocabulary and project mapping are in [docs/TAGS.md](docs/TAGS.md).

## Dates and source credit

The Gallery uses the compact `YYYY-MMDD` presentation used by the reference list. Each date is backed by a ledger that records what the date represents: for example, an original post timestamp, paper submission, repository creation, or version release. Those events are not treated as interchangeable first-publication claims. One entry without a recoverable dated source remains explicitly estimated in the ledger.

Every retained entry has source identifiers and linked evidence in [docs/SOURCES.md](docs/SOURCES.md). Source and media credit belong to the original authors, projects, and posts. This is a non-commercial curation, not an OpenAI resource, an experiment report, or a continuous monitoring service.

## Use and GitHub Pages

The Gallery is a static, self-contained site under `site/`; it has no API keys or backend. For local review, serve only that directory:

```bash
python -m pip install --requirement requirements.txt
python scripts/validate.py
python scripts/build.py
python -m unittest discover -s tests -v
python -m http.server 8765 --bind 127.0.0.1 --directory site
```

The included Pages workflow validates, builds, tests, and publishes only `site/` when manually dispatched after a maintainer configures GitHub Pages for their repository. No remote repository, deployment URL, or Pages site is claimed by this source package. See [docs/PUBLISHING.md](docs/PUBLISHING.md) for the maintainer checklist and [docs/SOCIAL_MEDIA_PLACEMENT.zh-CN.md](docs/SOCIAL_MEDIA_PLACEMENT.zh-CN.md) for the optional large Social-media files omitted from lightweight packages.

## Attribution and license

Discovery credit includes [Awesome Astra Embodied AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI) and [Awesome Robot Use Agent](https://github.com/kairunwen/Awesome-Robot-Use-Agent). Discovery lists are not presented as independent projects here.

MIT applies only to this repository's original curation and tooling. Linked papers, code, datasets, model weights, trademarks, and media remain under their respective terms. See [LICENSE](LICENSE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), and [CITATION.cff](CITATION.cff).
