# 检索覆盖与透明度

## 本次覆盖

核心问题是：近期有哪些**明确涉及 GPT-6 / GPT6 / Astra** 的机器人控制、具身评测、仿真构建和演示，证据能追溯到哪一层？主窗口为 2026-08-18 至 2026-09-18。

| 平台 | 实际取得的资料 | 本次不能声称的覆盖 |
| --- | --- | --- |
| GitHub | 仓库 README / 索引正文、项目结构、部分发布说明与许可说明 | 未克隆并审计所有文件；不提供实时 star 排名 |
| Hugging Face | 多个数据卡、模型卡、数据明细说明、少数文件索引 | 未下载完整数据/权重；没有完成运行验证 |
| X / Twitter | 作者贴文镜像、转引和定向搜索；少数已定位 status URL | 未连接登录态全量接口；未逐一播放完整原始视频 |
| 小红书 | 二手 Awesome 索引的作者 / 主题线索 | 没有取得可核验的原始笔记，不称已读原帖 |
| 知乎 | 中文讨论与链接线索 | 未由此建立新的独立已验证机器人实验 |
| 论文 / 项目站 | arXiv / HF 论文摘要、作者项目页、评测报告正文 | 没有逐页分析所有 PDF 或核查全部附件 |

部分页面直接读取失败时使用可读搜索正文，并在来源台账中记录 `search_text` 或 `partial_index`。这使目录可追溯，但不能消除搜索缓存陈旧、镜像转引或正文截断风险。

## 查询记录

`data/search-log.json` 保存 **34 条代表性实际查询**，不是逐次调用的完整日志。包括 exact URL 查询、作者名、模型拼写变体、GitHub/HF 项目名及中文平台定向检索。二手索引只用于发现，再尽可能回到一手资料。

可继续使用的 X 搜索式示例（执行结果取决于平台访问与索引）：

```text
("GPT-6" OR GPT6 OR Astra) (robot OR robotics OR embodied) since:2026-08-18 until:2026-09-19
from:kaiwynd ("GPT-6" OR GPT6 OR Astra) since:2026-08-18 until:2026-09-19
("GPT-6" OR Astra) (MuJoCo OR "Isaac Sim" OR real2sim OR policy) since:2026-08-18 until:2026-09-19
```

这里只给检索表达式；没有声称这些补充表达式全都独立执行过。日期 `until:2026-09-19` 用于覆盖 09-18 全日，仍以原帖绝对时间为准。

## 未升级为已验证结果的线索

RoboDojo 官方报告确认了入口和发布线索，但本次未读到完整量化正文；因此没有把中文媒体中的总分、成功率或硬件事故描述填入正式指标。后续应核对原报告及协议，而非复用新闻标题。[S013](SOURCES.md#s013)、[S015](SOURCES.md#s015)、[S048](SOURCES.md#s048)

知乎的 PhysBrain 中文讨论用于发现资源；技术描述回到项目页、仓库与数据卡核实，不把一篇转述算作新的实验。[S047](SOURCES.md#s047)、[S030](SOURCES.md#s030)

X 个别演示仅有昵称或主页，不编造 status ID；小红书 8 条均保留二手状态。详见目录中 C / D 标签。

## 发现来源致谢

[Awesome Astra Embodied AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI) 与 [Awesome Robot Use Agent](https://github.com/kairunwen/Awesome-Robot-Use-Agent) 帮助定位社区演示。原条目可能持续变化；本仓库使用原创摘要，保留来源与不确定性，不复制其全部文案和媒体。
