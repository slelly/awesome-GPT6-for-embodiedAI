# Awesome GPT6 Embodied AI

**GPT-6 Astra 具身智能项目、真实机器人实验、仿真评测与社区演示的证据分层目录。**

[English / 默认入口](README.md) · [Gallery 画廊](site/index.html) · [完整目录](docs/CATALOG.md) · [场景标签](docs/SCENE_TAGS.md) · [Astra 主题复核](docs/ASTRA_RELEVANCE_REVIEW.md) · [媒体台账](docs/MEDIA.md) · [公开社媒视频下载器](docs/SOCIAL_VIDEO_DOWNLOADER.md) · [Hugging Face 资源](docs/HUGGING_FACE.md) · [研究结论](docs/FINDINGS.md) · [贡献条目](CONTRIBUTING.md)

> 观察窗口：**2026-08-18 — 2026-09-18**。快照日期：**2026-09-18，Asia/Taipei**。这是一次截至当日的公开资料检索，不是持续监控或全网穷举。日期不明、较早基础设施和二手线索均单独标注。
>
> **不是 OpenAI 官方仓库。没有运行独立机器人实验；“来源核验”不等于“复现成功”。** GPT-6 编写控制代码、审查 VLA 动作、生成训练环境和真正在线控制机器人，分别记录，不混作一种能力。

## 收录概览

| 分层 | 数量 | 含义 |
| --- | ---: | --- |
| 核心项目与评测 | 12 | 与 GPT-6 具身应用直接相关；部分实施或日期仍待核 |
| 配套资源与对照 | 5 | harness、benchmark、理解类对照；不是新增 GPT-6 成果 |
| X / Twitter 线索 | 14 | 有作者镜像或二手索引；不能视作重复评测 |
| Hugging Face 资源 | 8 | 与项目交叉关联的数据/适配器；不重复计入 31 条目录 |

**31 条目录不等于 31 个已验证项目。** 两个 Awesome 汇总仓库及同一汇总仓库的 8 个锚点伪条目已从卡片目录移除，仍仅作为发现来源署名；其余真实独立项目即使参考资料中出现 Awesome 也保留。证据等级分布为 A: 13、B: 4、C: 12、D: 2；A 中也有纯基础设施和非交互评测。等级只描述来源：A 一手正文；B 部分一手；C 作者贴文镜像；D 二手发现线索。详见[收录方法](docs/METHODOLOGY.md)。

## 优先阅读：核心项目

条目名称的链接指向原始资源；“说明”链接包含控制接口、全部限制、事件日期依据及来源。

| 项目 | 环境 / GPT-6 的作用 | 已确认的资源与结果 | 核验边界 |
| --- | --- | --- | --- |
| [GPT-Policy](https://github.com/cheng-haha/GPT-Policy) | 真机；上下文学习 + 受约束工具控制 | 论文、代码预览、项目演示 | 许可 pending；不含完整私有实验资产；[A / P01](docs/CATALOG.md#p01) |
| [GPT-as-Policy](https://github.com/anonymous-report-421/GPT-as-Policy) | 仿真；Direct 与 π0.5 + GPT Hybrid | 同一 50-case 子集：Hybrid **48%**，Direct **26%**；代码、报告、HF 回放 | 不是与官方模型同 seed 重跑；[A / P02](docs/CATALOG.md#p02) |
| [Agent as Policy · AGP](https://agent-as-policy-2026.github.io/) | 真机；agent 观察、编程、控制、纠错 | 论文、演示、**162 条多模型 evaluated rows** 数据卡 | 162 不是 GPT-6 单模型次数；代码可访问性未确认；[A / P03](docs/CATALOG.md#p03) |
| [RoboCurve · Bowl & Puzzle](https://openai.robocurve.org/gpt-6-astra/) | 真机；末端位姿工具 + IK | Bowl **19/20**；Puzzle **2/20** | 两种任务差异很大；非盲评分等限制；[A / P04](docs/CATALOG.md#p04) |
| [StationeryBench](https://openai.robocurve.org/stationerybench/) | 真机双臂；五类文具操作 | Astra **7/100** 完成；平均进度 **46/100** | 不是 46% 成功率；VLA 对照的控制预算不同；[A / P05](docs/CATALOG.md#p05) |
| [RoboDojo · 官方 Astra 报告](https://robodojo-benchmark.com/report/gpt-6-astra-eval) | 真机 + 仿真；官方专项评测 | 确认报告入口与 09-16 公布线索 | 本次正文不完整，不转载未核对的总分/排名；[B / P06](docs/CATALOG.md#p06) |
| [ENPIRE](https://github.com/NVlabs/ENPIRE) | 真机；编程代理迭代策略与实验 | 可读框架代码；GPT-6 应用有作者演示线索 | 框架早于本月；不能将原论文实验都归给 GPT-6；[B / P07](docs/CATALOG.md#p07) |
| [GPT6-real2sim](https://github.com/lingxiao-guo/GPT6-real2sim) | 仿真；视频 → MuJoCo / Blender | DROID / YAM 重建和保存轨迹检查工具 | 包含失败、拟合与真实接触的不同情形；[A / P08](docs/CATALOG.md#p08) |
| [Real2Sim_GPT6_ASTRA](https://github.com/hku-sail/Real2Sim_GPT6_ASTRA) | 视觉重放；三视角 RGB → 可编辑场景 | Blender 建模 / 轨迹重建代码 | 绑定与动画插值 ≠ 物理控制成功；[A / P09](docs/CATALOG.md#p09) |
| [Real2Gym](https://cskrren.github.io/real2gym-site/) | 仿真工程；场景 / 本体重建 | 一手项目页和代码链接 | 未逐文件核验链接代码；[B / P10](docs/CATALOG.md#p10) |
| [dexgpt](https://github.com/Hu-xiao-max/dexgpt) | 仿真；手部视频重建线索 | 仓库身份和作者演示链接 | 实施、许可和重复实验待核；[B / P11](docs/CATALOG.md#p11) |
| [Drone-Bench](https://andonlabs.com/evals/drone-bench) | 仿真 / 硬件展示；无人机相关代码任务 | 官方页面已有 Astra 结果入口 | 基准更早；本次 Astra 更新日不明确；[A / P12](docs/CATALOG.md#p12) |

**同名消歧：** `cheng-haha/GPT-Policy`、`anonymous-report-421/GPT-as-Policy` 与 `Agent as Policy (AGP)` 是不同项目。旧 `GPT-Policy-Eval` 入口不重复计数。[来源 S001](docs/SOURCES.md#s001) · [S003](docs/SOURCES.md#s003) · [S005](docs/SOURCES.md#s005)

## 按你要研究的问题进入

| 目标 | 建议先看 | 理由 |
| --- | --- | --- |
| GPT + VLA 混合控制及失败纠正 | [P02](docs/CATALOG.md#p02)、[HF03](docs/HUGGING_FACE.md) | 对齐案例、方法对照、轨迹回放入口 |
| 真机上下文学习 / 在线编程控制 | [P01](docs/CATALOG.md#p01)、[P03](docs/CATALOG.md#p03) | 上下文、工具调用、执行反馈；注意公开资产边界 |
| 真实成功率及能力边界 | [P04](docs/CATALOG.md#p04)、[P05](docs/CATALOG.md#p05) | 固定任务重复试验，并记录失败 |
| 可迁移评测 harness | [Inspect Robots](https://github.com/robocurve/inspect-robots)、[RoboDojo](https://github.com/robodojo-benchmark/RoboDojo) | 控制接口和评测协议基础设施，而非另一个单独成绩 |
| GPT 帮助 Real2Sim / 仿真工程 | [P08](docs/CATALOG.md#p08) 至 [P11](docs/CATALOG.md#p11) | 区分物理接触、运动拟合、动画重放 |
| 从演示到小模型执行 | [Show-Harness](https://github.com/showlab/Show-Harness) | 配套工作；未确认 GPT-6 专项成绩，不冒充本模型成果 |
| “physical brain”究竟测什么 | [PhysBrain 1.5](https://deepcybo-physai.github.io/PhysBrain-1.5/) | 理解类对照与真实 action success 分开解释 |

这是一份策展阅读顺序，不是对不同协议结果的排行榜。配套资源详见[完整目录](docs/CATALOG.md)。Awesome 集合仅保留为发现来源，不作为独立项目卡片。

## X / Twitter 与知乎

X 线索覆盖物理键盘、网线插接、画图、移动操作、G1 导航/抓取、灵巧手解魔方/转笔、CARLA 和仿真控制等主题。社媒页签中的 12 项已核验到原始 status URL；未找到原帖的条目明确不显示作者主页或搜索页替代链接。详见 [X01–X14](docs/CATALOG.md#x01) 与 [原帖核验台账](docs/SOCIAL_LINKS.md)。

知乎取得的主要是中文讨论和资源转述，没有据此新增独立已验证机器人实验。逐平台检索覆盖、入口和失败边界见[检索记录](docs/SEARCH.md)。

## 本地使用

直接打开 `site/index.html` 即可使用中英文 Gallery；语言优先级是手动选择（浏览器记忆）→ 浏览器支持语言中的第一个可用语言 → 英文。页面数据内嵌、无第三方 JavaScript 或 API key；少数有出处的媒体会从原始公开主机加载，失败时明确回退。若使用轻量交付包，请先按[社媒原始媒体放置说明](docs/SOCIAL_MEDIA_PLACEMENT.zh-CN.md)将 14 个原文件复制至 `site/assets/social/`；无需改名。

```bash
# 仅使用 Python 3.10+ 标准库；不安装机器人/模型依赖
python scripts/validate.py
python scripts/build.py
python -m unittest discover -s tests -v

# 可选：本机浏览，默认绑定环回地址
python -m http.server 8765 --bind 127.0.0.1
# 浏览器打开 http://127.0.0.1:8765/site/
```

修改 `data/projects.json` / `data/sources.json` 后重新 build。生成的 CSV 是机器可读目录，不是执行脚本。远程链接检查是可选独立命令，不在默认 CI 中调用；本仓库不自动运行任何真实机器人或付费模型。

## 仓库结构

```text
awesome-gpt6-embodied/
├── README.md / README.en.md       中英入口
├── data/                         项目、来源、HF 资源、检索记录、CSV
├── docs/
│   ├── CATALOG.md / SOURCES.md    全量卡片与来源台账
│   ├── FINDINGS.md                综合结论及可检验研究问题
│   ├── HUGGING_FACE.md            数据 / 模型 / 资产地图
│   ├── METHODOLOGY.md / SEARCH.md 收录规则与检索覆盖
│   ├── REPRODUCIBILITY.md         复现依赖与安全边界
│   ├── PUBLISHING.md              GitHub / Pages 发布步骤
│   └── VALIDATION.md              本地验证记录
├── site/                         无依赖、可离线筛选的静态网页
├── scripts/                      构建、数据校验、可选外链检查
├── tests/                        离线单元测试
└── .github/                      CI、条目提交 / 勘误模板
```

## 维护与发布

当前是可上传 GitHub 的源码包，**尚未创建或推送远程仓库**。发布见 [PUBLISHING.md](docs/PUBLISHING.md)；贡献见 [CONTRIBUTING.md](CONTRIBUTING.md)。新增条目必须保留模型角色、证据、日期依据、许可和未决问题，而不只粘贴视频。

感谢 [Awesome Astra Embodied AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI) 与 [Awesome Robot Use Agent](https://github.com/kairunwen/Awesome-Robot-Use-Agent) 提供发现线索。本目录另行追溯项目页、代码说明和数据卡；不把两个索引视作两个独立实验来源。

**许可：** 本仓库原创整理及工具代码采用 [MIT](LICENSE)。链接的论文、代码、模型、数据、商标和媒体仍按其各自许可；没有复制第三方仓库、模型权重、字体或视频。条目写“公开可读”不自动等于允许商业使用。[第三方说明](THIRD_PARTY_NOTICES.md)
