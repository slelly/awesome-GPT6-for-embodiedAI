# 场景标签 / Scene tags

更新日期：2026-09-20。卡片仅显示 sim、real 或两者；标签描述一手材料中已经发生或已经覆盖的工作场景，不是未来用途、复现状态或可靠性评级。

## 分布

- sim：21 项（含 5 项同时有 real）
- real：18 项（含 5 项同时有 sim）
- 仅 sim：16 项；仅 real：13 项；两者：5 项

## 逐项依据

| 标签 | 条目 | 依据 |
| --- | --- | --- |
| real | P01, P03, P04, P05 | 一手项目页/仓库记录真实机器人执行或真机试验：[S001](SOURCES.md#s001)、[S005](SOURCES.md#s005)、[S010](SOURCES.md#s010)、[S011](SOURCES.md#s011)。 |
| real | P07 | ENPIRE 一手框架材料是实际机器人实验框架；Astra 专项接入仍另行待核：[S018](SOURCES.md#s018)。 |
| real | P12 | 官方 Drone-Bench 说明低成本无人机硬件和真实办公环境任务；不将其写为端到端飞行成功率：[S025](SOURCES.md#s025)。 |
| real | P18, P19, X15 | RoboHarm 仓库/发布视频、RoboFind 论文真机试验和 Wuji2 原帖视频分别提供实机场景证据：[S053](SOURCES.md#s053)、[S055](SOURCES.md#s055)、[S056](SOURCES.md#s056)、[S057](SOURCES.md#s057)。 |
| real | X01, X02, X03, X04 | 保留的作者材料分别声称物理键盘、网线插入、绘画和移动操作；原帖/日志不足但场景本身为真机：[S036](SOURCES.md#s036)、[S037](SOURCES.md#s037)、[S038](SOURCES.md#s038)。 |
| sim | P02, P08, P09, P10, P11, P17 | 资料分别明确 RoboDojo、MuJoCo/Blender 接触回放、Blender 视觉重放、Blender/MuJoCo 工作流、视频到手部仿真及 half-physics 基准：[S003](SOURCES.md#s003)、[S020](SOURCES.md#s020)、[S021](SOURCES.md#s021)、[S022](SOURCES.md#s022)、[S023](SOURCES.md#s023)、[S032](SOURCES.md#s032)。 |
| sim | X05–X14 | 作者材料明确 Isaac Sim、MuJoCo、CARLA 或仿真场景；没有据此升级为真机：[S039](SOURCES.md#s039)、[S038](SOURCES.md#s038)、[S040](SOURCES.md#s040)、[S024](SOURCES.md#s024)、[S042](SOURCES.md#s042)、[S043](SOURCES.md#s043)、[S033](SOURCES.md#s033)。 |
| sim, real | P06 | 官方报告声称覆盖 RoboDojo、类人高层控制和灵巧操作；完整正文仍不可得，故具体配置待核：[S013](SOURCES.md#s013)。 |
| sim, real | P13, P14, P16 | 一手材料明确提供真实/仿真任务或跨本体执行/评测接口：[S026](SOURCES.md#s026)、[S027](SOURCES.md#s027)、[S016](SOURCES.md#s016)。 |
| sim, real | P15 | 官方项目页称微调结合真实机器人轨迹与仿真经验；网页评分本身不是控制成功率：[S030](SOURCES.md#s030)。 |

## 待核边界

- P06 的两个标签来自官方报告所称覆盖范围；报告正文、具体任务与执行配置尚未完整取得，不能由此推导真机表现。
- X01–X04 的真机标签来自作者/镜像材料所描述的物理场景；原帖、代码和重复试验仍不完整。
- P07 的真机标签描述 ENPIRE 框架已发生的真实机器人实验，不把它自动延伸为已核实的 Astra 真机结果。
