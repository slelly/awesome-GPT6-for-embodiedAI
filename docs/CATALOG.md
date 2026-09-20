# 完整目录 / Full catalogue

证据快照：2026-09-20。本文件由 `scripts/build.py` 生成；请编辑 `data/projects.json`。

**A/B/C/D 是来源证据等级，不是模型能力、代码质量或独立复现等级。所有条目均未由本仓库独立运行机器人实验。**

A：一手正文可读；B：一手入口存在但关键实施/模型关系不完整；C：作者演示的可读镜像；D：二手索引。A 也可能没有公开代码。

“核心”仅代表与主题直接相关；不等于证据全部完整，也不保证日期均精确落在窗口内。

## 核心项目与评测 · 14

<a id="p01"></a>
### P01 · GPT-Policy · In-Context Robot Learning

固定 VLM 从示教、目标图像和交互历史中适应任务，经受约束的机器人工具闭环执行。

**来源等级：A** · 真机 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Dongzhou Cheng et al.  
**事件日期：** 2026-09-16（窗口内）  
**日期依据：** README：论文、项目页及代码发布日；首批演示为 09-11  
**入口：** [https://github.com/cheng-haha/GPT-Policy](https://github.com/cheng-haha/GPT-Policy)  
**代码入口：** [https://github.com/cheng-haha/GPT-Policy](https://github.com/cheng-haha/GPT-Policy)  
**许可状态：** 项目许可 pending；公开预览不授予再分发/商业使用  
**控制接口 / 作用：** 相机/状态/上下文 → Cartesian targets / waypoints → IK 校验 → ARX X5 或 I2RT/YAM

**限制与未决项：** 真实评测记录、私有提示和现场标定不随代码完整提供。 README 的少量条件任务 100% 不等于整体通用成功率。 RoboDojo 完整仿真管线仍列在 TODO。

paper：[https://arxiv.org/abs/2609.19138](https://arxiv.org/abs/2609.19138)  
project：[https://cheng-haha.github.io/GPT-Policy/](https://cheng-haha.github.io/GPT-Policy/)  
legacy：[https://github.com/cheng-haha/GPT-Policy-Eval](https://github.com/cheng-haha/GPT-Policy-Eval)  

**来源：** [S001 · GPT-Policy public implementation](SOURCES.md#s001) · [S002 · In-Context Robot Learning with VLM Agents](SOURCES.md#s002)

---

<a id="p02"></a>
### P02 · GPT-as-Policy · GPT-6 Direct / π0.5 Hybrid

在对齐 RoboDojo cases 上比较 GPT 直接控制与审查/修正 π0.5 动作；同时提供 RoboLab 展示入口。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Jiayi Su, Yixin Zheng et al.  
**事件日期：** 2026-09（仅确认到月份）  
**日期依据：** 月级公开快照；不把报道日期、账号建立日期当成代码首发日  
**入口：** [https://github.com/anonymous-report-421/GPT-as-Policy](https://github.com/anonymous-report-421/GPT-as-Policy)  
**代码入口：** [https://github.com/anonymous-report-421/GPT-as-Policy](https://github.com/anonymous-report-421/GPT-as-Policy)  
**许可状态：** 项目自有代码 MIT；数据 CC BY 4.0；上游资产/模型另计  
**控制接口 / 作用：** Direct：GPT 工具动作；Hybrid：π0.5 提案 + GPT 审查/可选修正

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Hybrid success | 48 % | 50 aligned cases | 10 tasks ×5 cases |
| Direct success | 26 % | 50 aligned cases | same selected case definitions |
| Hybrid mean Score | 62.6 score | 50 cases | native task score aggregation |
| Direct mean Score | 37.81 score | 48 cases with native scores | not same score denominator as success |
| GPT correction fraction | 14.4 % of executed control steps | hybrid executed steps | not token/API cost savings |

**限制与未决项：** 公开模型对照为重加权参考，不是同 seed 重新评测。 不能把这个 50-case 子集与官方 42-task 榜直接排名。 模拟器、OpenPI/JAX、checkpoint、授权模型账户需另行准备。

project：[https://anonymous-report-421.github.io/public-website/?lang=zh&view=1](https://anonymous-report-421.github.io/public-website/?lang=zh&view=1)  
dataset：[https://huggingface.co/datasets/YuMoool/astra-robodojo-rollouts](https://huggingface.co/datasets/YuMoool/astra-robodojo-rollouts)  

**来源：** [S003 · GPT 6 Astra as an Embodied Policy](SOURCES.md#s003) · [S004 · GPT-as-Policy source-release notes](SOURCES.md#s004) · [S045 · GPT-as-Policy rollout dataset](SOURCES.md#s045) · [S050 · GPT-as-Policy public website source](SOURCES.md#s050)

---

<a id="p03"></a>
### P03 · Agent as Policy（AGP）

真实双臂环境中由通用 agent 观察、编程、发出控制命令并利用执行反馈修正。

**来源等级：A** · 真机 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Mengzhao Jia, Yang Lin, Xixin Zhang et al.  
**事件日期：** 2026-09-11（窗口内）  
**日期依据：** HF 论文元数据；数据 b01/b02 分别冻结于 09-13/09-14，宣传帖更晚  
**入口：** [https://agent-as-policy-2026.github.io/](https://agent-as-policy-2026.github.io/)  
**代码入口：** [https://github.com/agent-as-policy-2026/agent-as-policy-2026](https://github.com/agent-as-policy-2026/agent-as-policy-2026)  
**许可状态：** 数据 CC BY 4.0；数据卡声明代码 Apache-2.0，但代码公开可访问性未确认  
**控制接口 / 作用：** 相机工具 → agent 生成程序 → Cartesian / joint commands → 机器人反馈

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| GPT-6 pooled completion (mixed conditions) | 123 successes | 130 | DETAILS 汇总；任务/effort/工具/知识条件混合，不是与其他模型同任务分布的受控比较 |

**限制与未决项：** 代码地址由数据卡链接；DETAILS 仍写 private until publication，不标记“代码已可复现”。 162 是当前数据卡全部模型 evaluated rows；62、112、196 属于不同页面/版本/口径。 不可将作者精选演示或部分配置成功率推广到全部任务。 DETAILS 中 GPT-6 的 123/130 是混合条件汇总；其他模型几乎仅测试 twopairs，禁止把总体比例当公平模型排名。

paper：[https://arxiv.org/abs/2609.12541](https://arxiv.org/abs/2609.12541)  
dataset：[https://huggingface.co/datasets/Agent-as-Policy/agent-as-policy](https://huggingface.co/datasets/Agent-as-Policy/agent-as-policy)  
x：[https://x.com/JillJia6/status/2100275532378317038](https://x.com/JillJia6/status/2100275532378317038)  

**来源：** [S005 · Agent as Policy project page](SOURCES.md#s005) · [S006 · Agent as Policy evaluated-trial dataset](SOURCES.md#s006) · [S007 · Agent as Policy dataset details](SOURCES.md#s007) · [S009 · Agent as Policy paper listing](SOURCES.md#s009) · [S044 · AGP author announcement, mirror](SOURCES.md#s044)

---

<a id="p04"></a>
### P04 · RoboCurve · Bowl & Puzzle

在 YAM 机械臂上测试粗粒度抓放与精细插入，提供逐次试验及失败边界。

**来源等级：A** · 真机 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Achu Menon et al. / Robocurve  
**事件日期：** 2026-09-04（窗口内）  
**日期依据：** 主报告署日  
**入口：** [https://openai.robocurve.org/gpt-6-astra/](https://openai.robocurve.org/gpt-6-astra/)  
**代码入口：** [https://github.com/robocurve/inspect-robots](https://github.com/robocurve/inspect-robots)  
**许可状态：** 评测框架 MIT；视频/报告版权另计  
**控制接口 / 作用：** 三相机+状态 → 绝对末端位姿/夹爪命令；medium，20 次模型调用上限，25% speed cap

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Bowl completion | 19 successes | 20 | one task |
| Puzzle completion | 2 successes | 20 | one task |

**限制与未决项：** 非盲评、人工重置；不同模型运行日/部分 rig 不同。 19/20 不能代表所有具身任务。


**来源：** [S010 · RoboCurve GPT-6 Astra two-task evaluation](SOURCES.md#s010) · [S026 · Inspect Robots](SOURCES.md#s026)

---

<a id="p05"></a>
### P05 · StationeryBench · 五类真实双臂文具任务

标记笔、纸夹、直尺、便签和盒子组成多阶段双臂任务；同时公布任务进度与完全完成率。

**来源等级：A** · 真机 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Zihan Jack Zhang et al. / Robocurve  
**事件日期：** 2026-09-10（窗口内）  
**日期依据：** 主报告署日  
**入口：** [https://openai.robocurve.org/stationerybench/](https://openai.robocurve.org/stationerybench/)  
**代码入口：** [https://github.com/robocurve/stationerybench](https://github.com/robocurve/stationerybench)  
**许可状态：** 任务仓库 MIT；报告/媒体按原许可  
**控制接口 / 作用：** GPT：末端位姿工具；MolmoAct2：10 Hz joint action chunks

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Astra full completion | 7 successes | 100 | 5 tasks ×20 trials |
| Astra mean progress | 46 out of 100 | 100 graded trials | human graded milestones |
| MolmoAct2 full completion | 0 successes | 100 | zero-shot checkpoint, different action/time budget |

**限制与未决项：** 46 是进度均值，不能写成 46% 成功率。 非盲评；两模型 action/time budget、部分 rig 不同；MolmoAct2 无任务微调。 仓库 mock 是抽象环境，不是物理仿真；scripted oracle 的成功不属于 GPT-6。


**来源：** [S011 · GPT-6 Astra vs MolmoAct2 on StationeryBench](SOURCES.md#s011) · [S012 · StationeryBench task registry](SOURCES.md#s012)

---

<a id="p06"></a>
### P06 · RoboDojo · 官方 GPT-6 Astra 评测报告

官方报告与作者宣布的评测覆盖 RoboDojo、类人机器人高层控制及灵巧操作；正文获取不完整。

**来源等级：B** · 真机 + 仿真 · GPT-6 明确，但正文证据不完整

**作者 / 团队：** RoboDojo team  
**事件日期：** 2026-09-16（窗口内）  
**日期依据：** 检索摘要中的报告日期；原页完整正文不可得  
**入口：** [https://robodojo-benchmark.com/report/gpt-6-astra-eval](https://robodojo-benchmark.com/report/gpt-6-astra-eval)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 已检索片段称 RoboProbe L3 固定控制接口；完整配置待核

**限制与未决项：** 保留官方入口，但不将二手报道的分数写进已核验指标表。 未确认专用 RoboProbe 代码的公开地址。 不声称 GPT-6 当前榜首；榜单与代码持续更新。

x：[https://x.com/MarioChan2002/status/2100091875403469014](https://x.com/MarioChan2002/status/2100091875403469014)  
benchmark：[https://github.com/robodojo-benchmark/RoboDojo](https://github.com/robodojo-benchmark/RoboDojo)  

**来源：** [S013 · RoboDojo Astra evaluation report](SOURCES.md#s013) · [S014 · RoboDojo Astra author announcement on X](SOURCES.md#s014) · [S015 · Mirror of RoboDojo author announcement](SOURCES.md#s015)

---

<a id="p07"></a>
### P07 · ENPIRE · GPT-6 机器人自主实验线索

NVIDIA 的真实机器人实验框架；GPT-6 特定应用来自作者演示声明，框架本体早于本窗口。

**来源等级：B** · 真机 · 作者声明，经镜像获取

**作者 / 团队：** NVlabs / Tonghe Zhang et al.  
**事件日期：** 2026-09-09（二手/作者报告时间）  
**日期依据：** 社区索引给出的 GPT6 演示日；精确原帖日期待核  
**入口：** [https://github.com/NVlabs/ENPIRE](https://github.com/NVlabs/ENPIRE)  
**代码入口：** [https://github.com/NVlabs/ENPIRE](https://github.com/NVlabs/ENPIRE)  
**许可状态：** Apache-2.0；第三方组件另计  
**控制接口 / 作用：** reset → execute → verify → record → refine；CaP / RL / BC 等可用

**限制与未决项：** 不能把整个 ENPIRE 论文实验默认当成 GPT-6 结果。 依赖现场标定、感知、机器人服务及 reset/reward 函数。 并非只输入一句 prompt 即获得完全独立真机系统。

project：[https://research.nvidia.com/labs/gear/enpire/](https://research.nvidia.com/labs/gear/enpire/)  
x_profile：[https://x.com/TongheZhang01](https://x.com/TongheZhang01)  

**来源：** [S018 · ENPIRE official code](SOURCES.md#s018) · [S019 · ENPIRE GPT6 author post mirrored in timeline](SOURCES.md#s019)

---

<a id="p08"></a>
### P08 · GPT6-real2sim · DROID / YAM 重建

由演示重建场景、标定及接触回放；代码同时保留不成功的物理重放。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Lingxiao Guo  
**事件日期：** 2026-09（仅确认到月份）  
**日期依据：** 月级公开快照；不采用第三方抓取时间为首发日  
**入口：** [https://github.com/lingxiao-guo/GPT6-real2sim](https://github.com/lingxiao-guo/GPT6-real2sim)  
**代码入口：** [https://github.com/lingxiao-guo/GPT6-real2sim](https://github.com/lingxiao-guo/GPT6-real2sim)  
**许可状态：** 需逐项检查第三方资产及仓库许可  
**控制接口 / 作用：** 多视角 RGB / 机器人动作 → MuJoCo 接触仿真 + Blender 渲染

**限制与未决项：** YAM microphones 的 contact-only attachment 失败；reference 视觉拟合不可替代成功。 归档回放验证不等于重新执行动力学实验。 部分原始数据须自行取得。


**来源：** [S020 · GPT6-real2sim](SOURCES.md#s020)

---

<a id="p09"></a>
### P09 · Real2Sim_GPT6_ASTRA · 三视角几何重放

从三路 RGB 重建可编辑 Blender 场景与动作动画，公开建模、拟合及验证代码。

**来源等级：A** · 视觉动画重放 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Kaixin Ding, Linjing You, Hengshuang Zhao  
**事件日期：** 2026-09（仅确认到月份）  
**日期依据：** 月级公开快照  
**入口：** [https://github.com/hku-sail/Real2Sim_GPT6_ASTRA](https://github.com/hku-sail/Real2Sim_GPT6_ASTRA)  
**代码入口：** [https://github.com/hku-sail/Real2Sim_GPT6_ASTRA](https://github.com/hku-sail/Real2Sim_GPT6_ASTRA)  
**许可状态：** 项目/机器人资产各自许可需核对  
**控制接口 / 作用：** RGB → 估计相机/尺度/几何/轨迹 → Blender 重放

**限制与未决项：** 无真实关节、深度、标定或动力学输入，不能称物理参数精确恢复。 夹持和释放包含姿态绑定及动画插值。 原始帧不在仓库中。


**来源：** [S021 · Real2Sim GPT6 ASTRA](SOURCES.md#s021)

---

<a id="p10"></a>
### P10 · Real2Gym

项目页展示真人/机器人视频到可执行机器人仿真的工作流，结合 Blender 与 MuJoCo。

**来源等级：B** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Real2Gym contributors  
**事件日期：** 2026-09（仅确认到月份）  
**日期依据：** 本月项目快照；首发日未确认  
**入口：** [https://cskrren.github.io/real2gym-site/](https://cskrren.github.io/real2gym-site/)  
**代码入口：** [https://github.com/cskrren/Real2Gym](https://github.com/cskrren/Real2Gym)  
**许可状态：** 未核实  
**控制接口 / 作用：** 真实演示 → 场景重建/动作重定向 → 仿真执行与场景变化

**限制与未决项：** 项目页明确链接代码；本次未读到完整仓库，环境安装和资源完备性待核。 不能把视觉匹配自动等同于新场景闭环泛化。


**来源：** [S022 · Real2Gym project](SOURCES.md#s022)

---

<a id="p11"></a>
### P11 · dexgpt · 手部视频到仿真

已定位作者的 dexgpt 仓库；44-DoF 手部跟踪、IK 和抓取细节仍主要来自作者社交演示。

**来源等级：B** · 仿真 · 作者声明，经镜像获取

**作者 / 团队：** xiao hu / Hu-xiao-max  
**事件日期：** 2026-09-09（二手/作者报告时间）  
**日期依据：** 社区索引给出日期，原帖日未独立确认  
**入口：** [https://github.com/Hu-xiao-max/dexgpt](https://github.com/Hu-xiao-max/dexgpt)  
**代码入口：** [https://github.com/Hu-xiao-max/dexgpt](https://github.com/Hu-xiao-max/dexgpt)  
**许可状态：** 未核实  
**控制接口 / 作用：** 作者声称：视频 → hand tracking → IK retargeting → grasp refinement

**限制与未决项：** 只确认仓库身份，未检查完整实现、数据或安装流程。 不声称已完成独立物理验证。

x_profile：[https://x.com/huxiao93612565](https://x.com/huxiao93612565)  

**来源：** [S023 · dexgpt repository](SOURCES.md#s023) · [S024 · Dexgpt and paused Go1 demos: author posts in mirror](SOURCES.md#s024) · [S051 · Dexgpt author post mirrored with repository link](SOURCES.md#s051)

---

<a id="p12"></a>
### P12 · Drone-Bench · Astra 更新

评测模型编写无人机感知与控制程序的能力，官方页面已列入 gpt-6-astra。

**来源等级：A** · 仿真 / 硬件演示 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Andon Labs  
**事件日期：** 未确认（首发/更新时间未确认）  
**日期依据：** 未确认首发日；2026-09-18 检索快照  
**入口：** [https://andonlabs.com/evals/drone-bench](https://andonlabs.com/evals/drone-bench)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 编码 agent → 五项独立子任务代码；局部控制系统执行

**限制与未决项：** 基准本体早于本窗口；Astra 更新的确切日未确认。 每项输入上游干净参考产物，10 次反馈提交取最佳；不是一次端到端飞行成功率。 页面旧 Discussion 与动态图更新可能不同步，不转录媒体的“全部超过人类”结论。 仅收录评测研究，不提供对未经同意人员的跟踪部署指导。


**来源：** [S025 · Drone-Bench official evaluation](SOURCES.md#s025)

---

<a id="p18"></a>
### P18 · RoboHarm · 机器人危险指令拒绝评测

在五类固定危险场景中比较 GPT-6 Astra、Claude Fable 5.1 与 MolmoAct2 是否尝试、拒绝或完成有害指令，并保留三机位视频与转录的事后标注流程。

**来源等级：A** · 真机 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Edward Sun, Sravanthi Machcha, Sabrina Zou, Tzu Kit Chan, Jay Chooi / RoboCurve  
**事件日期：** 2026-09-19（窗口内）  
**日期依据：** 发布帖 status ID 2101118049944543545 的 X Snowflake 时间为 2026-09-19T01:15:54Z；公开代码仓同日更新  
**入口：** [https://github.com/robocurve/roboharm](https://github.com/robocurve/roboharm)  
**代码入口：** [https://github.com/robocurve/roboharm](https://github.com/robocurve/roboharm)  
**许可状态：** 仓库声明 All rights reserved，不授予开源许可；第三方组件另依其条款  
**控制接口 / 作用：** 三相机与本体状态 → Inspect Robots agent/VLA policy → YAM 双臂动作；Astra/Fable 为 medium effort、40 次模型调用上限与 25% 速度限制

**限制与未决项：** 公开仓库提供任务、采集与标注工具，但不包含 raw rollouts，也不是冻结结果数据集。 报告入口本轮无法直接读取，因此不把视频中的汇总图转写为结构化排名指标。 五个固定场景与固定措辞不能代表开放环境安全性；复现实验应使用惰性替代物，禁止制造真实刀具、电器、压力或化学危险。

project：[https://robocurve.org/roboharm/](https://robocurve.org/roboharm/)  
post：[https://x.com/chooi_jeq/status/2101118049944543545](https://x.com/chooi_jeq/status/2101118049944543545)  

**来源：** [S053 · RoboHarm benchmark and collection toolkit](SOURCES.md#s053) · [S054 · RoboHarm research report entry point](SOURCES.md#s054) · [S055 · RoboHarm author release post and supplied video](SOURCES.md#s055)

---

<a id="p19"></a>
### P19 · RoboFind · 面向视障用户的个性化物品搜索

手机端一次性教授个人物品，Unitree Go2 执行搜索，验证与恢复 agent 在候选停点核对实例身份并决定完成或继续搜索；GPT-6 Astra 用于目标画像与导航指令，并设独立 Astra-only 对照。

**来源等级：A** · 真机 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Ruiping Liu, Shaofang Quan, Qian Yin et al.  
**事件日期：** 2026-09-17（窗口内）  
**日期依据：** arXiv v1 首次提交时间 2026-09-17T13:04:23Z  
**入口：** [https://arxiv.org/abs/2609.20330](https://arxiv.org/abs/2609.20330)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 论文 CC BY 4.0；正文称代码与结果将公开，但本轮未定位对应公开实现  
**控制接口 / 作用：** 手机教学视频 → GPT-6 Astra 目标画像/导航指令 → Uni-NaVid 驱动 Go2 搜索 → Grounding DINO + DINOv2 验证 → 固定恢复动作后继续搜索

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| RoboFind success | 17 successes | 20 | 十个目标各两次真机任务；含验证与恢复 |
| Sequential first-stop success | 5 successes | 20 | 从同一批 RoboFind 轨迹重建，不是另行执行的 baseline |
| GPT-6 Astra-only success | 5 successes | 12 | 六个共享目标上的独立执行；RoboFind 在同一目标子集为 10/12 |

**限制与未决项：** Sequential baseline 由 RoboFind 运行的首个稳定候选重建，不能描述为独立复跑。 GPT-6 Astra-only 仅覆盖六个共享目标、12 次运行；不同分母不能与完整 20 次 RoboFind 结果直接合并。 论文未提供公开代码或公开视频入口；卡片封面来自论文第 4 页 Fig. 3，不是视频首帧。

paper：[https://arxiv.org/abs/2609.20330](https://arxiv.org/abs/2609.20330)  

**来源：** [S056 · RoboFind paper and PDF](SOURCES.md#s056)

---

## 配套资源与对照 · 5

<a id="p13"></a>
### P13 · Inspect Robots

真实/仿真任务与多类策略共用的可审计评测框架，是 RoboCurve 报告的执行基础。

**来源等级：A** · 真机 + 仿真 · 基础设施，不是单独的 GPT-6 成果

**作者 / 团队：** Robocurve  
**事件日期：** 未确认（首发/更新时间未确认）  
**日期依据：** 未确认首发日；2026-09-18 检索快照  
**入口：** [https://github.com/robocurve/inspect-robots](https://github.com/robocurve/inspect-robots)  
**代码入口：** [https://github.com/robocurve/inspect-robots](https://github.com/robocurve/inspect-robots)  
**许可状态：** MIT  
**控制接口 / 作用：** policy × embodiment × task；日志包含配置、动作和评判

**限制与未决项：** 框架本体不算新的独立 GPT-6 成功案例。 默认安全检查不构成硬件安全认证。


**来源：** [S026 · Inspect Robots](SOURCES.md#s026)

---

<a id="p14"></a>
### P14 · Show-Harness

将离散语义动作交给本体解释器，附示教采集、训练、模型和数据。

**来源等级：A** · 真机 + 仿真 · 未确认 GPT-6 专项结果

**作者 / 团队：** Show Lab @ NUS  
**事件日期：** 2026-09（仅确认到月份）  
**日期依据：** README 月级 release  
**入口：** [https://github.com/showlab/Show-Harness](https://github.com/showlab/Show-Harness)  
**代码入口：** [https://github.com/showlab/Show-Harness](https://github.com/showlab/Show-Harness)  
**许可状态：** HF Qwen adapters/data Apache-2.0；Gemma adapter 受 Gemma terms 约束；代码许可需单独核对  
**控制接口 / 作用：** 图像 → MV_* / GRASP / RELEASE / DONE → 确定性运动解释器

**限制与未决项：** 未建立 GPT-6 专项结果；不是已证实的 Astra benchmark。 小模型权重不是 GPT-6 权重，也不据此断言为 GPT-6 蒸馏。 不同本体方向约定和 chat template 需核对。

project：[https://showlab.github.io/Show-Harness/](https://showlab.github.io/Show-Harness/)  
paper：[https://arxiv.org/abs/2609.10522](https://arxiv.org/abs/2609.10522)  

**来源：** [S027 · Show-Harness](SOURCES.md#s027) · [S028 · Show-Harness model adapters](SOURCES.md#s028) · [S029 · Show-Harness demonstration corpus](SOURCES.md#s029)

---

<a id="p15"></a>
### P15 · PhysBrain 1.5 / PhysBrainEvalKit

包含 GPT-6 作为对照的具身理解评测，以及独立开源模型和动作/未来状态展示。

**来源等级：A** · 非交互评测 · GPT-6 仅作对照

**作者 / 团队：** DeepCybo team  
**事件日期：** 2026-09（仅确认到月份）  
**日期依据：** 本月项目与报告快照；不采纳搜索引擎异常首发时间  
**入口：** [https://deepcybo-physai.github.io/PhysBrain-1.5/](https://deepcybo-physai.github.io/PhysBrain-1.5/)  
**代码入口：** [https://github.com/DeepCybo-PhysAI/PhysBrain-1.5](https://github.com/DeepCybo-PhysAI/PhysBrain-1.5)  
**许可状态：** 未核实  
**控制接口 / 作用：** 本条对比口径为具身理解输出，而非 GPT6 控制机器人成功率

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| GPT-6 embodied-understanding mean | 73.3 out of 100 | 28 benchmarks | project-reported unweighted mean; not action success |

**限制与未决项：** 28-benchmark 均值不可与 StationeryBench 或 RoboDojo 成功率合并。 模型的动作输出能力与这张理解榜不是同一评测结论。

evalkit：[https://github.com/DeepCybo-PhysAI/PhysBrainEvalKit](https://github.com/DeepCybo-PhysAI/PhysBrainEvalKit)  
project：[https://deepcybo-physai.github.io/PhysBrain-1.5/](https://deepcybo-physai.github.io/PhysBrain-1.5/)  

**来源：** [S030 · PhysBrain 1.5 project](SOURCES.md#s030) · [S031 · PhysBrain 1.5 code/report entry](SOURCES.md#s031)

---

<a id="p16"></a>
### P16 · RoboDojo / XPolicyLab 基础设施

统一模拟和真机操作评测；RoboDojo 负责环境，XPolicyLab 负责策略侧集成。

**来源等级：A** · 真机 + 仿真 · 基础设施，不是单独的 GPT-6 成果

**作者 / 团队：** RoboDojo contributors  
**事件日期：** 2026-09-16（本月更新，基础项目更早）  
**日期依据：** 09-16 至 09-17 维护更新；原始基准发布于 07-06  
**入口：** [https://github.com/robodojo-benchmark/RoboDojo](https://github.com/robodojo-benchmark/RoboDojo)  
**代码入口：** [https://github.com/robodojo-benchmark/RoboDojo](https://github.com/robodojo-benchmark/RoboDojo)  
**许可状态：** 待核冲突：README 正文为非商业研究许可，GitHub UI 标签显示 MIT  
**控制接口 / 作用：** 策略服务器 ↔ 仿真客户端；状态/动作协议按本体配置

**限制与未决项：** 09-16/17 更新涉及 observation 时序、RGB byte order 与 swap_T 资产，应固定代码和数据版本。 不要直接混用旧评测快照与新资产。 商业使用前必须解决许可文本不一致。


**来源：** [S016 · RoboDojo official code](SOURCES.md#s016) · [S017 · RoboDojo project site](SOURCES.md#s017)

---

<a id="p17"></a>
### P17 · HumanCLAW

人形机器人导航与交互基准；社区存在 Astra 演示线索，但本条只确认基准本体。

**来源等级：A** · 仿真 · 二手来源提及

**作者 / 团队：** HumanCLAW contributors  
**事件日期：** 2026-07-29（窗口外背景）  
**日期依据：** 论文日期，明确早于本窗口  
**入口：** [https://github.com/Human-CLAW/HumanCLAW](https://github.com/Human-CLAW/HumanCLAW)  
**代码入口：** [https://github.com/Human-CLAW/HumanCLAW](https://github.com/Human-CLAW/HumanCLAW)  
**许可状态：** 未核实  
**控制接口 / 作用：** 抽象动作/技能与 half-physics 环境

**限制与未决项：** 不能把原基准其他模型结果认作 GPT-6。 代码、权重与环境 release checklist 未完成；不标记“一键可复现”。


**来源：** [S032 · HumanCLAW benchmark](SOURCES.md#s032)

---

## X / Twitter 演示线索 · 15

<a id="x01"></a>
### X01 · 真实机器人键盘打字

作者展示约 40 分钟探索后的物理按键；视频为加速播放。

**来源等级：C** · 真机 · 作者声明，经镜像获取

**作者 / 团队：** @kaiwynd  
**事件日期：** 2026-09-12（二手/作者报告时间）  
**日期依据：** 索引给出的演示日期；具体原帖 URL 由用户于 2026-09-19 补充，本轮未独立核实其内容或绝对时间  
**入口：** [https://x.com/kaiwynd/status/2098823484474348008](https://x.com/kaiwynd/status/2098823484474348008)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 单演示，无重复成功率；不是电脑键盘 API 的 computer use。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/kaiwynd/status/2098823484474348008](https://x.com/kaiwynd/status/2098823484474348008)  

**来源：** [S036 · Kaifeng keyboard and Ethernet author posts, mirror](SOURCES.md#s036)

---

<a id="x02"></a>
### X02 · 真实网线插入

作者称约 2 小时、4 次人类提示介入后完成网线插入。

**来源等级：C** · 真机 · 作者声明，经镜像获取

**作者 / 团队：** @kaiwynd  
**事件日期：** 未确认（首发/更新时间未确认）  
**日期依据：** 只取得相对时间或二手索引；不强行换算首发日  
**入口：** [https://x.com/kaiwynd/status/2099524132341711051](https://x.com/kaiwynd/status/2099524132341711051)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 不能称完全无人干预，也不能用剪辑时长估计延迟。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/kaiwynd/status/2099524132341711051](https://x.com/kaiwynd/status/2099524132341711051)  

**来源：** [S036 · Kaifeng keyboard and Ethernet author posts, mirror](SOURCES.md#s036)

---

<a id="x03"></a>
### X03 · 机械臂画金门大桥

作者给机器人画笔和相机，通过多次尝试完成语义目标绘画。

**来源等级：C** · 真机 · 作者声明，经镜像获取

**作者 / 团队：** @cdngdev  
**事件日期：** 2026-09-08（二手/作者报告时间）  
**日期依据：** 索引给出的演示日期，原帖绝对时间未独立核实  
**入口：** [https://x.com/cdngdev/status/2097339677128982873](https://x.com/cdngdev/status/2097339677128982873)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 演示不是重复评测；完整机器人控制脚本未核实。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/cdngdev/status/2097339677128982873](https://x.com/cdngdev/status/2097339677128982873)  

**来源：** [S037 · Robot painting author post, mirror](SOURCES.md#s037)

---

<a id="x04"></a>
### X04 · 跨场景移动操作 ICL

作者展示不同视角/布局下从视频推断移动操作。

**来源等级：C** · 真机 · 作者声明，经镜像获取

**作者 / 团队：** @ax_pey  
**事件日期：** 2026-09-11（二手/作者报告时间）  
**日期依据：** 索引给出的演示日期，原帖绝对时间未独立核实  
**入口：** [https://x.com/ax_pey/status/2098216469012283681](https://x.com/ax_pey/status/2098216469012283681)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** “无任务文字提示”不意味着没有系统提示、工具定义或控制先验。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/ax_pey/status/2098216469012283681](https://x.com/ax_pey/status/2098216469012283681)  

**来源：** [S038 · Mobile manipulation and G1 navigation author posts, mirror](SOURCES.md#s038)

---

<a id="x05"></a>
### X05 · G1 可乐瓶抓取

作者展示 Codex/Astra 在 Isaac Sim 控制 G1，并明确回复使用 IK。

**来源等级：C** · 仿真 · 作者声明，经镜像获取

**作者 / 团队：** @RotekSong  
**事件日期：** 2026-09-13（二手/作者报告时间）  
**日期依据：** 索引给出的演示日期，原帖绝对时间未独立核实  
**入口：** [https://x.com/RotekSong/status/2099104628562608371](https://x.com/RotekSong/status/2099104628562608371)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 模型规划与低层全身控制应分开评估，不能称纯模型关节闭环。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/RotekSong/status/2099104628562608371](https://x.com/RotekSong/status/2099104628562608371)  

**来源：** [S039 · G1 bottle pickup and Sharpa RL author posts, mirror](SOURCES.md#s039)

---

<a id="x06"></a>
### X06 · G1 导航

作者展示 GPT-6 生成导航行为与场景的仿真演示。

**来源等级：C** · 仿真 · 作者声明，经镜像获取

**作者 / 团队：** @RotekSong  
**事件日期：** 2026-09-11（二手/作者报告时间）  
**日期依据：** 索引给出的演示日期，原帖绝对时间未独立核实  
**入口：** [https://x.com/RotekSong/status/2098212303263183329](https://x.com/RotekSong/status/2098212303263183329)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 低层轨迹跟踪器负责哪些动作、是否在线重规划待核。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/RotekSong/status/2098212303263183329](https://x.com/RotekSong/status/2098212303263183329)  

**来源：** [S038 · Mobile manipulation and G1 navigation author posts, mirror](SOURCES.md#s038)

---

<a id="x07"></a>
### X07 · 灵巧手解魔方

作者声明 Astra 解魔方；个人主页确认存在对应 MuJoCo 双手项目。

**来源等级：C** · 仿真 · 作者声明，经镜像获取

**作者 / 团队：** @ZeYanjie  
**事件日期：** 2026-09-10（二手/作者报告时间）  
**日期依据：** 索引给出的演示日期，原帖绝对时间未独立核实  
**入口：** 原帖未找到；不以作者主页或搜索页替代  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 完整控制方式与在线/离线搜索协议未核实，不直接标“真机零样本”。 未独立复现；原帖/完整日志/代码状态需继续核实。

x_profile：[https://x.com/ZeYanjie](https://x.com/ZeYanjie)  
demo：[https://dex-rubik-cube.yanjieze.com/](https://dex-rubik-cube.yanjieze.com/)  
x_search：[https://x.com/search?q=from%3AZeYanjie%20%28%22GPT-6%22%20OR%20GPT6%20OR%20Astra%29%20since%3A2026-08-18%20until%3A2026-09-19&f=live](https://x.com/search?q=from%3AZeYanjie%20%28%22GPT-6%22%20OR%20GPT6%20OR%20Astra%29%20since%3A2026-08-18%20until%3A2026-09-19&f=live)  

**来源：** [S040 · Yanjie Ze project directory](SOURCES.md#s040) · [S041 · Dex Rubik GPT6 author post, mirror](SOURCES.md#s041)

---

<a id="x08"></a>
### X08 · Sharpa 灵巧手转笔 PPO

作者展示学生 Chengyang Li 用 Astra 构建 Isaac Lab 任务并训练转笔策略。

**来源等级：C** · 仿真 · 作者声明，经镜像获取

**作者 / 团队：** @walterzhu8  
**事件日期：** 2026-09-16（二手/作者报告时间）  
**日期依据：** 索引给出的演示日期，原帖绝对时间未独立核实  
**入口：** [https://x.com/walterzhu8/status/2100212420840989112](https://x.com/walterzhu8/status/2100212420840989112)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 控制机器人的是训练得到的策略；不是 GPT-6 在线以关节频率输出动作。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/walterzhu8/status/2100212420840989112](https://x.com/walterzhu8/status/2100212420840989112)  

**来源：** [S039 · G1 bottle pickup and Sharpa RL author posts, mirror](SOURCES.md#s039)

---

<a id="x09"></a>
### X09 · Go1 暂停物理的关节控制

作者描述每次推理暂停物理，250 次推理对应 5 秒仿真运动。

**来源等级：C** · 仿真 · 作者声明，经镜像获取

**作者 / 团队：** @sri299792458  
**事件日期：** 未确认（首发/更新时间未确认）  
**日期依据：** 只取得相对时间或二手索引；不强行换算首发日  
**入口：** [https://x.com/sri299792458/status/2097349207795335424](https://x.com/sri299792458/status/2097349207795335424)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 模拟 50 Hz 关节目标不等于墙钟 50 Hz 实时 GPT 控制。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/sri299792458/status/2097349207795335424](https://x.com/sri299792458/status/2097349207795335424)  

**来源：** [S024 · Dexgpt and paused Go1 demos: author posts in mirror](SOURCES.md#s024)

---

<a id="x10"></a>
### X10 · CARLA 视觉路点驾驶

作者展示相机图像到短期路点；局部控制器再输出转向、油门和刹车。

**来源等级：C** · 仿真 · 作者声明，经镜像获取

**作者 / 团队：** @ludocomito  
**事件日期：** 未确认（首发/更新时间未确认）  
**日期依据：** 只取得相对时间或二手索引；不强行换算首发日  
**入口：** [https://x.com/ludocomito/status/2097329417760440461](https://x.com/ludocomito/status/2097329417760440461)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 没有受控成功率；仿真演示不建立道路行驶安全。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/ludocomito/status/2097329417760440461](https://x.com/ludocomito/status/2097329417760440461)  

**来源：** [S042 · CARLA Astra author post, mirror](SOURCES.md#s042)

---

<a id="x11"></a>
### X11 · 双机器人抛接球

作者展示 MuJoCo 抛接球仿真。

**来源等级：C** · 仿真 · 作者声明，经镜像获取

**作者 / 团队：** @thermalpastor  
**事件日期：** 未确认（首发/更新时间未确认）  
**日期依据：** 只取得相对时间或二手索引；不强行换算首发日  
**入口：** [https://x.com/thermalpastor/status/2097496200631210136](https://x.com/thermalpastor/status/2097496200631210136)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 模型是否在每个决策步在线调用尚未核实；不按真机动态控制计。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/thermalpastor/status/2097496200631210136](https://x.com/thermalpastor/status/2097496200631210136)  

**来源：** [S043 · Juggling and bicycle author posts, mirror](SOURCES.md#s043)

---

<a id="x12"></a>
### X12 · G1 自行车控制代码

作者称 Astra 帮助编写并调试 MuJoCo 自行车控制代码。

**来源等级：C** · 仿真 · 作者声明，经镜像获取

**作者 / 团队：** @thermalpastor  
**事件日期：** 未确认（首发/更新时间未确认）  
**日期依据：** 只取得相对时间或二手索引；不强行换算首发日  
**入口：** [https://x.com/thermalpastor/status/2097802933429796873](https://x.com/thermalpastor/status/2097802933429796873)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 生成控制代码与模型实时平衡策略不同。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/thermalpastor/status/2097802933429796873](https://x.com/thermalpastor/status/2097802933429796873)  

**来源：** [S043 · Juggling and bicycle author posts, mirror](SOURCES.md#s043)

---

<a id="x13"></a>
### X13 · Dual-ALOHA 空间约束演示

双臂空间约束演示线索。

**来源等级：D** · 仿真 · 二手来源提及

**作者 / 团队：** @qineng_wang  
**事件日期：** 2026-09-15（二手/作者报告时间）  
**日期依据：** 索引给出的演示日期，原帖绝对时间未独立核实  
**入口：** [https://x.com/qineng_wang/status/2099893504658866561](https://x.com/qineng_wang/status/2099893504658866561)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 尚未核实原始协议；需区分计划回放与在线策略。 未独立复现；用户补充的原帖链接、完整日志与代码状态仍需独立核实。


**来源：** [S033 · Awesome Astra Embodied AI discovery collection](SOURCES.md#s033) · [S052 · Dual-ALOHA original-post URL supplied by user](SOURCES.md#s052)

---

<a id="x14"></a>
### X14 · 办公场景 → Newton / G1

办公场景仿真构建线索。

**来源等级：D** · 仿真 · 二手来源提及

**作者 / 团队：** @Jiarui_X  
**事件日期：** 2026-09-11（二手/作者报告时间）  
**日期依据：** 索引给出的演示日期，原帖绝对时间未独立核实  
**入口：** [https://x.com/Jiarui_X/status/2098439950991806804](https://x.com/Jiarui_X/status/2098439950991806804)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 需核实是场景工程还是 GPT6 在线控制。 未独立复现；原帖/完整日志/代码状态需继续核实。

post：[https://x.com/Jiarui_X/status/2098439950991806804](https://x.com/Jiarui_X/status/2098439950991806804)  

**来源：** [S033 · Awesome Astra Embodied AI discovery collection](SOURCES.md#s033)

---

<a id="x15"></a>
### X15 · Wuji2 灵巧手视觉自扶正

作者演示 GPT-6 Astra Ultra 根据第三人称 RGB 反馈，让倒卧的 Wuji2 灵巧手用手指支撑并站立；视频同时展示加速片段与正常速度片段。

**来源等级：B** · 真机 · GPT-6 明确，但正文证据不完整

**作者 / 团队：** Zhiyang (Frank) Dou  
**事件日期：** 2026-09-18（窗口内）  
**日期依据：** 原帖 status ID 2100754714971287557 的 X Snowflake 时间为 2026-09-18T01:12:08Z  
**入口：** [https://x.com/frankzydou/status/2100754714971287557](https://x.com/frankzydou/status/2100754714971287557)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 用户提供原帖视频用于本站展示；未取得代码、模型输出或更广泛再许可  
**控制接口 / 作用：** 第三人称 RGB 相机反馈 → Astra Ultra 迭代控制 → Wuji2 灵巧手手指接触与姿态调整

**限制与未决项：** 原帖页面在本轮环境返回 403；视频与精确 status URL 已匹配，但完整提示、工具接口和运行日志未公开。 单次剪辑包含 16× 加速，不构成重复成功率或实时控制延迟证据。 未独立复现硬件控制，也未核验断电后保持姿态的时长。

post：[https://x.com/frankzydou/status/2100754714971287557](https://x.com/frankzydou/status/2100754714971287557)  
project：[https://frank-zy-dou.github.io/blog/wuji2-hand-stands-up/](https://frank-zy-dou.github.io/blog/wuji2-hand-stands-up/)  

**来源：** [S057 · Wuji2 hand self-righting author post and supplied video](SOURCES.md#s057) · [S058 · Zhiyang Dou research note: robotic hand self-righting](SOURCES.md#s058)

---
