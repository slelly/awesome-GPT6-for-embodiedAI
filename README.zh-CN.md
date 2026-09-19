# Awesome GPT6 Embodied AI

一份有来源边界的中英双语目录，收录 GPT-6 Astra 相关的具身智能项目、评测、工作流资源与可追溯的社区演示。

[English（默认入口）](README.md) · [Gallery 画廊](site/index.html) · [来源](docs/SOURCES.md) · [媒体](docs/MEDIA.md) · [标签](docs/TAGS.md) · [日期台账](docs/PUBLICATION_DATES.md) · [贡献](CONTRIBUTING.md)

## 目录

- [收录内容](#收录内容)
- [按工作流标签浏览](#按工作流标签浏览)
- [日期与来源署名](#日期与来源署名)
- [本地使用与 GitHub Pages](#本地使用与-github-pages)
- [署名与许可](#署名与许可)

## 收录内容

本快照包含 31 条：17 个 Projects 和 14 个 Social 原帖线索。画廊将两者分组展示，并在各组内按日期倒序；存在时，卡片会保留直达 Paper、Code、Project page 或 Post 的链接。

目录借鉴 [Awesome Astra Embodied AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI) 便于访客浏览的写法：按工作流组织、显式来源署名、突出日期。必要差异是：本仓库保留逐项证据台账，并区分直接项目、配套资源和社媒线索。

## 按工作流标签浏览

每张卡片将事实性的场景标签与一个或多个工作流标签组合。搜索框支持中文或英文项目名称、标签及多词 AND 匹配。

| 场景 | 工作流示例 |
| --- | --- |
| `仿真` / `simulation` | `控制`、`真转仿`、`重放`、`强化学习训练`、`物理仿真` |
| `真机` / `real world` | `控制`、`评测`、`策略`、`测试框架` |
| 跨场景 | `基准`、`代码生成`、`灵巧操作`、`环境构建` |

标签只描述保留材料中呈现的工作内容；不表示不同项目使用相同基准、部署条件或模型结论。完整词表与逐项映射见 [docs/TAGS.md](docs/TAGS.md)。

## 日期与来源署名

画廊采用参考仓库的紧凑 `YYYY-MMDD` 格式。每个日期在台账中保留其实际含义，例如原帖时间、论文提交、仓库创建或版本发布；这些事件不会被混写成同一种“首次发布”。一项没有可恢复日期入口的记录仍在台账明确标为估算。

每条记录都有来源 ID 与证据链接，详见 [docs/SOURCES.md](docs/SOURCES.md)。来源和媒体版权归原作者、项目及原帖所有。本目录不是 OpenAI 官方资源、独立实验报告或持续监控服务。

## 本地使用与 GitHub Pages

Gallery 是 `site/` 下的自包含静态网站，无后端和 API key。本地预览只需服务该目录：

```bash
python -m pip install --requirement requirements.txt
python scripts/validate.py
python scripts/build.py
python -m unittest discover -s tests -v
python -m http.server 8765 --bind 127.0.0.1 --directory site
```

随包提供的 Pages workflow 会在维护者手动触发后校验、构建、测试，并仅发布 `site/`。本源码包未创建远程仓库，也不虚构部署链接；发布前请在目标仓库配置 GitHub Pages。维护步骤见 [docs/PUBLISHING.md](docs/PUBLISHING.md)。轻量包省略的社媒原文件请按 [放置说明](docs/SOCIAL_MEDIA_PLACEMENT.zh-CN.md) 复制到指定位置。

## 署名与许可

发现线索感谢 [Awesome Astra Embodied AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI) 与 [Awesome Robot Use Agent](https://github.com/kairunwen/Awesome-Robot-Use-Agent)。发现列表不会在本目录中被当作独立项目重复收录。

MIT 仅适用于本仓库原创整理与工具；链接的论文、代码、数据集、模型权重、商标和媒体均遵循各自条款。参见 [LICENSE](LICENSE)、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 与 [CITATION.cff](CITATION.cff)。
