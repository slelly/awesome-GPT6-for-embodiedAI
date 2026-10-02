# 完整目录 / Full catalogue

证据快照：2026-10-02。本文件由 `scripts/build.py` 生成；请编辑 `data/projects.json`。

**A/B/C/D 是来源证据等级，不是模型能力、代码质量或独立复现等级。所有条目均未由本仓库独立运行机器人实验。**

A：一手正文可读；B：一手入口存在但关键实施/模型关系不完整；C：作者演示的可读镜像；D：二手索引。A 也可能没有公开代码。

“核心”仅代表与主题直接相关；不等于证据全部完整，也不保证日期均精确落在窗口内。

## 核心项目与评测 · 43

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

新论文把早期 RoboDojo 直接/混合策略结果扩展到夹爪、灵巧手、移动操作、导航、运动与人形全身任务；本卡合并同团队早期 GPT-as-Policy 发布，避免重复计算 48% 混合控制结果。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Galbot Team, Jiayi Su, Yixin Zheng et al.  
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
paper：[https://arxiv.org/abs/2609.38537](https://arxiv.org/abs/2609.38537)  

**来源：** [S003 · GPT 6 Astra as an Embodied Policy](SOURCES.md#s003) · [S004 · GPT-as-Policy source-release notes](SOURCES.md#s004) · [S045 · GPT-as-Policy rollout dataset](SOURCES.md#s045) · [S050 · GPT-as-Policy public website source](SOURCES.md#s050) · [S113 · Systematically Exploring GPT-6 Astra as Embodied Policies](SOURCES.md#s113)

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

**限制与未决项：** 代码地址由数据卡链接；DETAILS 仍写 private until publication，不标记“代码已可复现”。 162 是当前数据卡全部模型 evaluated rows；62、112、196 属于不同页面/版本/口径。 不可将作者精选演示或部分配置成功率推广到全部任务。 DETAILS 中 GPT-6 的 123/130 是混合条件汇总；其他模型几乎仅测试 twopairs，禁止把总体比例当公平模型排名。 2026-09-21 新增完整英文项目影片、更多任务预览与 provenance；不改变既有指标。

paper：[https://arxiv.org/abs/2609.12541](https://arxiv.org/abs/2609.12541)  
dataset：[https://huggingface.co/datasets/Agent-as-Policy/agent-as-policy](https://huggingface.co/datasets/Agent-as-Policy/agent-as-policy)  
x：[https://x.com/JillJia6/status/2100275532378317038](https://x.com/JillJia6/status/2100275532378317038)  
video：[https://github.com/user-attachments/assets/788696b7-7461-4011-b58c-dce6ee930342](https://github.com/user-attachments/assets/788696b7-7461-4011-b58c-dce6ee930342)  

**来源：** [S005 · Agent as Policy project page](SOURCES.md#s005) · [S006 · Agent as Policy evaluated-trial dataset](SOURCES.md#s006) · [S007 · Agent as Policy dataset details](SOURCES.md#s007) · [S009 · Agent as Policy paper listing](SOURCES.md#s009) · [S044 · AGP author announcement, mirror](SOURCES.md#s044) · [S078 · Agent as Policy English-film update](SOURCES.md#s078)

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

9 月 21 日论文补充完整仿真评测：Astra 在 42 个任务、每任务 50 次、共 2,100 次试验上报告平均成功率 22.48%、Score 28.97。真机协议因不安全动作中止，保留的 33 次仅为诊断样本。

**来源等级：A** · 真机 + 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Wenbo Zhang, Kaixuan Wang, Yutao Ouyang et al.  
**事件日期：** 2026-09-16（窗口内）  
**日期依据：** 检索摘要中的报告日期；原页完整正文不可得  
**入口：** [https://robodojo-benchmark.com/report/gpt-6-astra-eval](https://robodojo-benchmark.com/report/gpt-6-astra-eval)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 论文 arXiv non-exclusive distribution license；不是 CC BY 或通用再利用许可。图 2 仅用于本地审核预览，公开再发布许可未确认。  
**控制接口 / 作用：** 固定 LLM 通过 move_eef 选择末端目标，非学习后处理转换为关节轨迹；不是 25 Hz 模型推理。

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| RoboDojo Average success rate | 22.48 % | 42 tasks × 50 episodes = 2,100 trials; one evaluation seed | arXiv v1 Table 1; leaderboard Average is axis-averaged. Public policy snapshot is dated 2026-09-10 and was not rerun with the LLM task text. |
| RoboDojo Average Score | 28.97 score / 100 | 5 capability-axis averages from the same 2,100 Astra trials | Mean process reward × 100; not success rate. Episode-pooled Score is 28.72, distinct from the reported leaderboard Average. |

**限制与未决项：** 未独立复现；主评测每模型一个 seed，无重复种子方差。 GPT-5.5 同为 50 次/任务；DeepSeek-Flash 为 10 次/任务，不能混用分母。 公开策略基线为 2026-09-10 榜单快照，未以 LLM 所获文字输入重新运行。 真机协议中止，12 任务、33 次为选择性诊断材料，不是正式 RoboDojo-Real 成绩。

x：[https://x.com/MarioChan2002/status/2100091875403469014](https://x.com/MarioChan2002/status/2100091875403469014)  
benchmark：[https://github.com/robodojo-benchmark/RoboDojo](https://github.com/robodojo-benchmark/RoboDojo)  
paper：[https://arxiv.org/abs/2609.24170](https://arxiv.org/abs/2609.24170)  

**来源：** [S013 · RoboDojo Astra evaluation report](SOURCES.md#s013) · [S014 · RoboDojo Astra author announcement on X](SOURCES.md#s014) · [S015 · Mirror of RoboDojo author announcement](SOURCES.md#s015) · [S064 · An Unexpected Robot Policy — arXiv v1](SOURCES.md#s064)

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

Real2Gym 将人类或机器人视频重建为可交互仿真环境，让智能体在仿真中生成、执行并提炼操作技能，再通过共享感知控制接口迁移到真实 Franka；新论文补充了与 GPT-6 Astra Direct Mode 的仿真和真机比较。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Kerui Ren, Yingxiang Xu, Kaiwen Song et al.  
**事件日期：** 2026-09-29（本月更新，基础项目更早）  
**日期依据：** arXiv:2609.37089 v1 was submitted 2026-09-29T09:16:49Z; the earlier repository and v5.3 workflow update predate the paper.  
**入口：** [https://real2gym.github.io/](https://real2gym.github.io/)  
**代码入口：** [https://github.com/real2gym/Real2Gym](https://github.com/real2gym/Real2Gym)  
**许可状态：** 论文为 arXiv non-exclusive distribution license；当前代码、依赖与资产许可需在复用前分别核对。  
**控制接口 / 作用：** 人类/机器人视频 → 可编辑 Real2Sim gym 与物理动作验证 → Astra 生成操作代码并从成败中提炼技能 → 共享视觉/控制接口适配仿真和真实 Franka

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Simulation success-rate gain over Astra Direct Mode | 16.7 percentage points | paper simulation evaluation environments | Real2Gym versus GPT-6 Astra Direct Mode; author-reported with approximately 74.9% fewer policy-execution tokens |
| Physical execution success-rate gain over Astra Direct Mode | 33.3 percentage points | four tasks on a real Franka robot | author-reported Real2Gym comparison |

**限制与未决项：** 论文摘要报告百分点提升，但未在摘要中给出每组原始成功次数；本站未独立复现实验。 四项 Franka 任务和作者构建的仿真环境不能代表开放世界机器人泛化。 完整系统同时改变环境重建、代码策略、经验提炼与执行接口，差异不能只归因于基础模型。

paper：[https://arxiv.org/abs/2609.37089](https://arxiv.org/abs/2609.37089)  
project：[https://real2gym.github.io/](https://real2gym.github.io/)  
code：[https://github.com/real2gym/Real2Gym](https://github.com/real2gym/Real2Gym)  
v5.3_update：[https://github.com/cskrren/Real2Gym/commit/b705ee9427af748fabdb3877d7678ce05b28de77](https://github.com/cskrren/Real2Gym/commit/b705ee9427af748fabdb3877d7678ce05b28de77)  

**来源：** [S022 · Real2Gym project](SOURCES.md#s022) · [S114 · Real2Gym arXiv paper and current project page](SOURCES.md#s114)

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
**许可状态：** 项目明确采用 CC BY-NC 4.0；原始视频与第三方依赖仍按各自权利边界处理。  
**控制接口 / 作用：** 三相机与本体状态 → Inspect Robots agent/VLA policy → YAM 双臂动作；Astra/Fable 为 medium effort、40 次模型调用上限与 25% 速度限制

**限制与未决项：** 公开仓库提供任务、采集与标注工具，但不包含 raw rollouts，也不是冻结结果数据集。 报告入口本轮无法直接读取，因此不把视频中的汇总图转写为结构化排名指标。 五个固定场景与固定措辞不能代表开放环境安全性；复现实验应使用惰性替代物，禁止制造真实刀具、电器、压力或化学危险。 2026-09-22 许可提交明确项目采用 CC BY-NC 4.0；实验数字与媒体未变。

project：[https://robocurve.org/roboharm/](https://robocurve.org/roboharm/)  
post：[https://x.com/chooi_jeq/status/2101118049944543545](https://x.com/chooi_jeq/status/2101118049944543545)  
license_commit：[https://github.com/robocurve/roboharm/commit/5952f0035037604265d5cf38fa24938d4acf7133](https://github.com/robocurve/roboharm/commit/5952f0035037604265d5cf38fa24938d4acf7133)  

**来源：** [S053 · RoboHarm benchmark and collection toolkit](SOURCES.md#s053) · [S054 · RoboHarm research report entry point](SOURCES.md#s054) · [S055 · RoboHarm author release post and supplied video](SOURCES.md#s055) · [S081 · RoboHarm license clarification](SOURCES.md#s081)

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

<a id="p20"></a>
### P20 · EmbodiedSWE · 长时程灵巧机器人编码智能体基准

GPT-6 Astra 通过 Codex 编写和迭代仿真任务解法。项目覆盖 28 个任务，报告 Astra 成功率 82%；页面未给出主评测逐模型运行分母，尚未独立复现。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Zeyu Shen, Haoxiang You, Yilang Liu et al.  
**事件日期：** 2026-09-20（窗口内）  
**日期依据：** 作者新闻明确标注 2026-09-20 released。  
**入口：** [https://embodiedswe.github.io/](https://embodiedswe.github.io/)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 项目媒体与代码许可未核实；本次未下载或重新托管视频。  
**控制接口 / 作用：** GPT-6 Astra writes and iterates simulation solutions through Codex. The project covers 28 tasks and reports 82% success for Astra; the page does not state the main evaluation run denominator. Not independently reproduced.

**限制与未决项：** 作者项目页自报；未独立复现。 未收到视频原文件，预览保留来源链接。 论文与博客仍标 soon；本轮发现时项目页 Code 链接返回 404，未作为可用代码按钮。 编码智能体生成解法，不应解读为高频端到端动作策略。


**来源：** [S059 · EmbodiedSWE project page](SOURCES.md#s059) · [S060 · Kashu Yamazaki news: EmbodiedSWE release](SOURCES.md#s060)

---

<a id="p21"></a>
### P21 · OpenArm Mona Lisa · LeRobot ACT 仿真绘画

HIM Astra 挑战中的 OpenArm 仿真绘画项目，结合脚本绘画序列与 ACT 关节策略。GPT-6 是构建助手；真机和真实颜料未测试，发布日期未知。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** HIM Arena user e  
**事件日期：** 未确认（首发/更新时间未确认）  
**日期依据：** 独立项目页未提供发布日期；2026-09-23 仅为本轮发现日。  
**入口：** [https://arena.himrobotics.com/uploads/source_59ffd3291f3623fc498d](https://arena.himrobotics.com/uploads/source_59ffd3291f3623fc498d)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 官方 HIM Arena 视频已下载并仅用于本地审核预览；项目媒体与代码的公开再利用许可仍未核实。  
**控制接口 / 作用：** An OpenArm simulation painting entry in the HIM Astra challenge combines a scripted painting sequence with an ACT joint policy. GPT-6 assists development; physical hardware and real paint are untested. Publication date unknown.

**限制与未决项：** 作者项目页自报；未独立复现。 已从官方 HIM Arena 项目页取得视频并在本地审核预览中实播；公开再利用许可未核实。 Physical Palette Runner 是同一成果前身，不另计卡片。 HIM 未审查或执行上传的项目代码；本轮也未运行。


**来源：** [S061 · OpenArm Mona Lisa — LeRobot ACT](SOURCES.md#s061) · [S063 · HIM GPT-6 Astra Challenge results](SOURCES.md#s063)

---

<a id="p22"></a>
### P22 · Fridge Speller · G1 字母磁贴拼词

在 MuJoCo 中，Unitree G1 与 Dex3-1 手行走至冰箱并用磁贴拼出 HELLO。作者称项目用 GPT-6 Astra 构建；仅报告单场景演示，未证明模型逐步直接控制，也无真机结果。发布日期未知。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Maddie D. Reese / HIM Arena  
**事件日期：** 未确认（首发/更新时间未确认）  
**日期依据：** 独立项目页未提供发布日期；2026-09-23 仅为本轮发现日。  
**入口：** [https://arena.himrobotics.com/uploads/source_62bc9b696cef9e7c64d6](https://arena.himrobotics.com/uploads/source_62bc9b696cef9e7c64d6)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 官方 HIM Arena 视频已下载并仅用于本地审核预览；项目媒体与代码的公开再利用许可仍未核实。  
**控制接口 / 作用：** A simulated Unitree G1 with Dex3-1 hands walks to a fridge and spells HELLO with magnets. The author credits GPT-6 Astra for building the project; this is a nominal-scene demo, without evidence of direct model control or real-hardware results. Publication date unknown.

**限制与未决项：** 作者项目页自报；未独立复现。 已从官方 HIM Arena 项目页取得视频；原响应末尾约 4.4 秒存在损坏，预览使用可解码的 226.234 秒审核转码。 五次放置属于一段演示，不是五次独立试验。 HIM 未审查或执行上传的项目代码；本轮也未运行。


**来源：** [S062 · Fridge Speller](SOURCES.md#s062) · [S063 · HIM GPT-6 Astra Challenge results](SOURCES.md#s063)

---

<a id="p23"></a>
### P23 · GPT-6-Astra Lights Up Embodied Navigation · 零样本连续环境导航

扩展报告让 GPT-6 Astra 仅凭单目 RGB 在 Codex harness 中自主选择观测、原子动作和停止时机；在固定 R2R-CE-100 上，medium/ultra 各单次运行报告 SR 76.0%/79.0%、SPL 67.9%/69.5%。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Guangzhao Dai, Qianru Sun, Qi Wu, Bin Zhu  
**事件日期：** 2026-09-17（本月更新，基础项目更早）  
**日期依据：** arXiv v1 submitted 2026-09-17; v2 followed on 2026-09-18.  
**入口：** [https://arxiv.org/abs/2609.29861](https://arxiv.org/abs/2609.29861)  
**代码入口：** [https://github.com/daiguangzhao/gpt-6-astra-for-vln](https://github.com/daiguangzhao/gpt-6-astra-for-vln)  
**许可状态：** 扩展报告采用 CC BY 4.0；项目网站仓库未声明独立代码许可。  
**控制接口 / 作用：** 512×512 单目 RGB + 指令/连续会话上下文 → Astra 自主调用 observe() 与 step(actions) → 0.25 m 前进、15° 转向、30° 俯仰或 STOP

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Ultra reasoning success rate | 79.0 % | 100 fixed R2R-CE validation-unseen episodes | one run per episode; explicit STOP within 3 m; 500 primitive-action / 2,400 s budget |
| Ultra reasoning SPL | 69.5 % | same 100 episodes | same single-run ultra evaluation |
| Medium reasoning success rate | 76.0 % | same 100 episodes | one run per episode under the same prompt, tools, and budgets |

**限制与未决项：** 每种 reasoning effort 对每个 episode 仅运行一次，未报告跨 seed 方差，本站未独立复现。 固定 100-episode 子集与训练方法使用的完整 val-unseen split 不同；论文也明确说明跨方法比较并非严格公平。 Ultra 的 21 个失败中有 13 个最终距目标至少 5 m；更高 reasoning effort 未消除路线保持与目标确认问题。 本条目合并同作者早期 arXiv:2609.20116 工作流研究，不另建重复卡片。

paper：[https://arxiv.org/abs/2609.29861](https://arxiv.org/abs/2609.29861)  
project：[https://daiguangzhao.github.io/gpt-6-astra-for-vln/](https://daiguangzhao.github.io/gpt-6-astra-for-vln/)  
earlier_report：[https://arxiv.org/abs/2609.20116](https://arxiv.org/abs/2609.20116)  

**来源：** [S065 · How Far Can GPT-6-Astra Go? arXiv paper](SOURCES.md#s065) · [S091 · GPT-6-Astra Lights Up Embodied Navigation report](SOURCES.md#s091) · [S092 · GPT-6-Astra for VLN official project repository](SOURCES.md#s092)

---

<a id="p24"></a>
### P24 · Benchmarking Frontier VLMs on Robots · Pantograph

在 6 台 Pandroid 双臂移动机器人上，以相同提示、工具和预算比较 Astra 与 Fable；官方页报告 Astra 完成率 36%、Fable 15%。

**来源等级：A** · 真机 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Pantograph  
**事件日期：** 2026-09-17（窗口内）  
**日期依据：** Pantograph research index dates the official report to 2026-09-17.  
**入口：** [https://pantograph.com/journal/vlm-harness](https://pantograph.com/journal/vlm-harness)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 报告和媒体版权归 Pantograph；本地仅保留官方社交预览图，未声明再许可。  
**控制接口 / 作用：** 统一 VLM harness → 离散工具调用 → Pandroid 双臂移动机器人

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Astra completion | 36 % | 80 rollouts | 8 tasks × 10 trials, 20-minute or 96-turn limit |
| Fable completion | 15 % | 80 rollouts | same harness and task budget |

**限制与未决项：** 作者自报，未独立复现。 8 个任务、每模型每任务 10 次，不能推广到其他硬件或任务。 网页精选成功/失败视频不是全部 160 次 rollout。

project：[https://pantograph.com/journal/vlm-harness](https://pantograph.com/journal/vlm-harness)  

**来源：** [S066 · Pantograph VLM robot harness report](SOURCES.md#s066)

---

<a id="p26"></a>
### P26 · Axol Pick-and-Pack · Astra 视觉复核

Astra 仅审阅相机图像，确定性 Python 规划与受保护的 Axol 控制代码执行动作；作者记录一次罐头入袋成功及随后扭矩安全中止。

**来源等级：A** · 真机 · 一手资料明确涉及 GPT-6

**作者 / 团队：** dineshreddy91  
**事件日期：** 2026-09-17（窗口内）  
**日期依据：** GitHub repository created 2026-09-17.  
**入口：** [https://github.com/dineshreddy91/robot-pick-pack](https://github.com/dineshreddy91/robot-pick-pack)  
**代码入口：** [https://github.com/dineshreddy91/robot-pick-pack](https://github.com/dineshreddy91/robot-pick-pack)  
**许可状态：** 仓库代码与证据图片的明确再许可未核实；本地图片仅供审核。  
**控制接口 / 作用：** 相机图像 → Astra 复核 → 确定性规划器 → 受保护 Axol 控制器

**限制与未决项：** 只记录一次成功抓取放袋，不能视为重复成功率。 回零因肩部扭矩残差 4.1 Nm 超过 4.0 Nm 限值而中止。 仓库没有公开视频。


**来源：** [S068 · Axol robot pick-and-pack repository](SOURCES.md#s068)

---

<a id="p28"></a>
### P28 · GPT-6 Astra Policy on DexJoCo

Astra 编写基于示例、图像和机器人状态的控制器，冻结代码后在三项 DexJoCo 任务和两种随机化条件下评测 900 episodes。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** YichengDraw  
**事件日期：** 2026-09-17（窗口内）  
**日期依据：** GitHub repository created 2026-09-17.  
**入口：** [https://github.com/YichengDraw/astra-policy-dexjoco](https://github.com/YichengDraw/astra-policy-dexjoco)  
**代码入口：** [https://github.com/YichengDraw/astra-policy-dexjoco](https://github.com/YichengDraw/astra-policy-dexjoco)  
**许可状态：** 代码 MIT；仓库演示媒体未见单独许可声明。  
**控制接口 / 作用：** 示例/观测/状态 → Astra 一次性生成控制器 → 冻结代码评测

**限制与未决项：** 评测阶段不逐步调用模型。 成功率应按任务与随机化条件分别读取，不能合并成单一通用分数。 三个成功样例视频不代表全部 900 次运行。


**来源：** [S070 · GPT-6 Astra policy on DexJoCo](SOURCES.md#s070)

---

<a id="p29"></a>
### P29 · Astra on RoboMME · 稀疏规划与视觉完成监控

三层长时程操作系统由 Astra 规划 grounded subtask、π0.5/MME-VLA 执行动作、Qwen3-VL-4B LoRA 判断何时再次规划。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Bingao Chen, Haoquan Fang, C. Karen Liu  
**事件日期：** 2026-09-21（窗口内）  
**日期依据：** Initial public repository release committed 2026-09-21 UTC.  
**入口：** [https://bingaochen.github.io/Astra-on-RoboMME/](https://bingaochen.github.io/Astra-on-RoboMME/)  
**代码入口：** [https://github.com/bingaochen/Astra-on-RoboMME](https://github.com/bingaochen/Astra-on-RoboMME)  
**许可状态：** 代码 Apache-2.0；Qwen、RoboMME、VLA 及媒体保持上游许可。  
**控制接口 / 作用：** Astra 规划 → π0.5/VLA action chunks → Qwen3-VL-4B 完成监控 → 按需再规划

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Overall success | 79.13 % | 800 official RoboMME test episodes | 633 success, 103 failure, 64 timeout |
| Mean Astra calls | 3.63 calls per episode | same 800 episodes | three-tier scheduler |

**限制与未决项：** 作者自报，未独立复现。 官方 test split 800 episodes 的结果依赖公开流程之外的模型/API与 GPU 环境。 79.13% 是整个三层系统结果，不是 Astra 单模型分数。

code：[https://github.com/bingaochen/Astra-on-RoboMME](https://github.com/bingaochen/Astra-on-RoboMME)  
weights：[https://huggingface.co/bingaochen/Astra-on-RoboMME-Monitor](https://huggingface.co/bingaochen/Astra-on-RoboMME-Monitor)  

**来源：** [S071 · Astra on RoboMME repository](SOURCES.md#s071)

---

<a id="p30"></a>
### P30 · RoboICL · 具身上下文学习

RoboICL 以统一的观测—动作—回执—观测语法组织示范与交互记忆，让冻结的 GPT-6 Astra 在 RoboDojo 与三项真机任务中从上下文适应；新发布论文扩展了早期九任务结果。

**来源等级：A** · 真机 + 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Fangcheng Liu, Yeqing Shen, Anda Cheng et al. / Mosi-AI  
**事件日期：** 2026-09-19（窗口内）  
**日期依据：** GitHub repository created 2026-09-19 UTC.  
**入口：** [https://mosi-ai.github.io/RoboICL-GPT6-Astra.github.io/](https://mosi-ai.github.io/RoboICL-GPT6-Astra.github.io/)  
**代码入口：** [https://github.com/Mosi-AI/RoboICL](https://github.com/Mosi-AI/RoboICL)  
**许可状态：** 项目代码以 MIT 许可发布；第三方子模块和基准资产适用各自许可，项目媒体未见统一再许可声明。  
**控制接口 / 作用：** 示范上下文 + 锚定交互记忆 + 当前视觉/状态 → GPT-6 Astra → 受限双臂末端动作 → 执行回执与新观测

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| RoboDojo 30-task overall score | 50.64 score | 30 tasks | zero-shot for Open tasks and one demonstration elsewhere; strongest reported baseline 33.68 |
| Three-shot real-robot mean progress | 78.89 score | 3 real-robot tasks | author-reported mean; zero-shot 14.45 and one-shot 63.33 |

**限制与未决项：** 论文和代码均为作者发布，本目录未独立复现模型调用、仿真或真机实验。 30-task 汇总混合 Open 零样本与其余类别一示范设置，不是统一 shot 数的单一协议。 真机结果只有三项任务；不同 shot 数的提升不能外推为跨机器人稳定收益。

paper：[https://arxiv.org/abs/2609.34261](https://arxiv.org/abs/2609.34261)  
code：[https://github.com/Mosi-AI/RoboICL](https://github.com/Mosi-AI/RoboICL)  

**来源：** [S072 · RoboICL repository](SOURCES.md#s072) · [S107 · RoboICL arXiv paper and official repository](SOURCES.md#s107)

---

<a id="p31"></a>
### P31 · GPT-6 LIBERO Manipulation Probe

把规划、2D/3D 定位和低层控制拆开评测；Astra 直接输出 7-D 末端增量，额外正交视角显著改善所测抓放任务。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Jacksonha7  
**事件日期：** 2026-09-23（窗口内）  
**日期依据：** GitHub repository created 2026-09-23 UTC.  
**入口：** [https://github.com/Jacksonha7/gpt6-libero-probe](https://github.com/Jacksonha7/gpt6-libero-probe)  
**代码入口：** [https://github.com/Jacksonha7/gpt6-libero-probe](https://github.com/Jacksonha7/gpt6-libero-probe)  
**许可状态：** 仓库许可状态未核实；本地证据图仅供审核预览。  
**控制接口 / 作用：** 多视角 RGB / 可选真值坐标 → Astra → 7-D 末端增量动作

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Ground-truth coordinate success | 37 successes | 40 | four pick-and-place tasks |
| Main/wrist-view success | 2 successes | 40 | same four tasks without privileged coordinates |
| Orthogonal-view success | 34 successes | 40 | same four tasks with added side view |

**限制与未决项：** 仅四项 LIBERO 抓放任务、每条件 40 次。 多视角与真值定位结果不应推广到一般具身任务。 公开媒体是对照 GIF，未见独立 MP4。


**来源：** [S073 · GPT-6 LIBERO manipulation probe](SOURCES.md#s073)

---

<a id="p33"></a>
### P33 · Robot-vLLM · GPT Planner + π₀.₅ + ROS 2

连接 GPT Planner、官方 OpenPI π₀.₅ 客户端与 ROS 2 执行/恢复，在四滑块共享感知实验中记录 12 seeds×3 组运行。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** nssmd  
**事件日期：** 2026-09-15（窗口内）  
**日期依据：** GitHub repository created 2026-09-15; v0.5.0 released the same day.  
**入口：** [https://github.com/nssmd/robot-vllm](https://github.com/nssmd/robot-vllm)  
**代码入口：** [https://github.com/nssmd/robot-vllm](https://github.com/nssmd/robot-vllm)  
**许可状态：** 代码 Apache-2.0；OpenPI、模型权重和仿真依赖另按上游许可。  
**控制接口 / 作用：** GPT-6 高层规划 → π₀.₅ 动作策略 → ROS 2 执行与恢复

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Valid completed runs | 33 successes | 36 | 12 seeds × 3 shared-perception groups; 3 infrastructure interruptions |

**限制与未决项：** 任务只验证简单视觉到达与共享感知，不代表复杂抓取或真机性能。 33 个有效成功与 3 个基础设施中断不能解释为 100% 无条件成功。 未找到公开视频。

release：[https://github.com/nssmd/robot-vllm/releases/tag/v0.5.0](https://github.com/nssmd/robot-vllm/releases/tag/v0.5.0)  

**来源：** [S075 · Robot-vLLM repository](SOURCES.md#s075)

---

<a id="p34"></a>
### P34 · quackd · 多机器人 LLM CLI / Harness

LLM 在声明的机器人 verbs 中逐步选动作；2026-09-15 的 SO-101 真机 wave 记录包含 10 次模型调用、8 个 verbs 和 97 条被接受命令。

**来源等级：A** · 真机 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Rok Benko  
**事件日期：** 2026-09-15（本月更新，基础项目更早）  
**日期依据：** quackd v0.9.0 and the public SO-101 experiment log were released 2026-09-15; author post followed 2026-09-16.  
**入口：** [https://github.com/rokbenko/quackd](https://github.com/rokbenko/quackd)  
**代码入口：** [https://github.com/rokbenko/quackd](https://github.com/rokbenko/quackd)  
**许可状态：** 项目代码按仓库许可；README GIF/PNG 未见独立媒体再许可声明，本地仅保留项目图用于审核。  
**控制接口 / 作用：** LLM → 机器人 verbs / JSON 命令 → quackd 适配器 → SO-101 真机

**限制与未决项：** 相机裁掉抬起的手臂，且每次结束机械臂都会掉落。 97 条命令被解析接受不等同于 97 次任务成功。 X 原帖正文访问受限；原帖作为同一项目来源合并，不单独建卡。

post：[https://x.com/rokbenko/status/2100234282631360540](https://x.com/rokbenko/status/2100234282631360540)  
package：[https://pypi.org/project/quackd/](https://pypi.org/project/quackd/)  

**来源：** [S076 · quackd repository and experiment log](SOURCES.md#s076) · [S077 · quackd SO-101 author post](SOURCES.md#s077)

---

<a id="p35"></a>
### P35 · RoboDawn · 冻结 VLM 闭环机器人控制

冻结 VLM 通过离散移动、旋转和夹爪命令闭环控制机器人，并用示范做上下文学习；GPT-6 Astra 的正式结果来自 RoboTwin 2.0 与 RoboDojo 仿真，论文真机表格使用 Gemini 3.8 Flash。

**来源等级：A** · 真机 + 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Meng-Hao Guo, Zhe-Han Mo, Jia-Jun Wang et al.  
**事件日期：** 2026-09-19（窗口内）  
**日期依据：** arXiv:2609.22966 v1 submitted 2026-09-19T11:34:13Z; public code followed on 2026-09-22.  
**入口：** [https://robodawn.top/](https://robodawn.top/)  
**代码入口：** [https://github.com/Hugo-AGI/RoboDawn](https://github.com/Hugo-AGI/RoboDawn)  
**许可状态：** 代码仓库为 MIT；论文为 arXiv non-exclusive distribution license，项目站回放媒体未见独立再许可声明。  
**控制接口 / 作用：** 多视角图像 + 机器人状态 + 任务/示范/历史 → 冻结 VLM 推理 → 离散语义动作 → 运动规划执行 → 反馈与记忆更新

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| RoboTwin 2.0 C2R zero-shot success | 53.2 % | 50 tasks × 10 episodes = 500 trials | GPT-6 Astra; no task demonstration and no parameter update |
| RoboTwin 2.0 C2R one-shot success | 73.6 % | 50 tasks × 10 episodes = 500 trials | GPT-6 Astra; one clean-scene demonstration in context and no parameter update |
| RoboDojo zero-shot success | 35.67 % | 42 tasks × 5 episodes = 210 trials | GPT-6 Astra; score 39.92; no task demonstration |
| RoboDojo one-shot success | 47.17 % | 42 tasks × 5 episodes = 210 trials | GPT-6 Astra; score 54.63; one task demonstration in context |
| Real Franka block-in-basket | 9 successes | 10 zero-shot trials | Gemini 3.8 Flash, not GPT-6 Astra |
| Real Franka block stacking | 5 successes | 10 zero-shot trials | Gemini 3.8 Flash, not GPT-6 Astra |
| Real Piper cloth folding | 0 successes | 10 zero-shot trials | Gemini 3.8 Flash, not GPT-6 Astra |

**限制与未决项：** Astra 的主要量化结果来自仿真；论文正式真机表格全部使用 Gemini 3.8 Flash，不能混写为 Astra 真机成绩。 项目演示浏览器含一条 Astra 在真实 Piper 上的折衣失败记录，但它不是论文正式真机成功率。 结果、代码和回放均未由本仓库独立复现；项目站所称 710 个评测 episode 与 128 个示范未逐条审计。 项目站视频可访问不等于获得再分发许可，本卡只保留论文机制图。

paper：[https://arxiv.org/abs/2609.22966](https://arxiv.org/abs/2609.22966)  
project：[https://robodawn.top/](https://robodawn.top/)  
results：[https://robodawn.top/results/](https://robodawn.top/results/)  

**来源：** [S082 · RoboDawn official project page and results browser](SOURCES.md#s082) · [S083 · RoboDawn technical report](SOURCES.md#s083) · [S084 · RoboDawn official code](SOURCES.md#s084)

---

<a id="p36"></a>
### P36 · DrivingBench · Astra 真实汽车闭环驾驶评测

DrivingBench 让 GPT-6 Astra 通过 observe、set_motion 与 stop_now 三个 MCP 工具闭环控制真实 Toyota Corolla；在同一对话的首次失败与反思后，第二次低速尝试完成 134.7 米锥桶路线。

**来源等级：A** · 真机 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Aditya Ramabadran, Simon Mahns, Tobias Gessler  
**事件日期：** 2026-09-18（本月更新，基础项目更早）  
**日期依据：** Official harness repository initial commit 2026-09-18T00:59:00Z; public benchmark discussion followed in the current review window.  
**入口：** [https://drivingbench.com/](https://drivingbench.com/)  
**代码入口：** [https://github.com/aditya-ramabadran/drivingbench_harness_v1](https://github.com/aditya-ramabadran/drivingbench_harness_v1)  
**许可状态：** Harness 为 MIT；官方站视频与画面未见独立再许可声明，本站仅远程引用官方预览图。  
**控制接口 / 作用：** 前向/广角相机 + 车速/方向盘遥测 → Astra/Codex → MCP 离散运动指令 → openpilot/comma four → 转向、加速与制动；人类驾驶员全程备刹车

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Astra best course progress | 100 % | attempt 2 of up to 3 attempts in one continuous chat | 134.7 m completed in 5:22; Codex medium; low-speed closed cone course |
| Astra first-attempt progress | 49 % | attempt 1 in the same continuous chat | 67.3 m, DNF; followed by a generic reflection prompt before attempt 2 |

**限制与未决项：** 每个模型只有一段连续对话中的最多三次相关尝试，不是多 seed 独立重复。 路线位于空停车场且速度很低，驾驶员全程准备制动；不能外推到公共道路自动驾驶。 Astra 第二次成功依赖首次尝试后的同上下文反思，首试成功率与 best-of-three 必须分开理解。 模型并非车载实时控制器；推理延迟、离散观察与 openpilot 执行层共同影响结果。

report：[https://drivingbench.com/report/](https://drivingbench.com/report/)  
trace：[https://drivingbench.com/trace/gpt-6-astra/2/](https://drivingbench.com/trace/gpt-6-astra/2/)  
code：[https://github.com/aditya-ramabadran/drivingbench_harness_v1](https://github.com/aditya-ramabadran/drivingbench_harness_v1)  
paper：[https://arxiv.org/abs/2609.38948](https://arxiv.org/abs/2609.38948)  

**来源：** [S085 · DrivingBench official benchmark, report, and Astra traces](SOURCES.md#s085) · [S086 · DrivingBench v1 harness](SOURCES.md#s086) · [S115 · DrivingBench arXiv paper](SOURCES.md#s115)

---

<a id="p37"></a>
### P37 · Astra Robot Sim2Real · 电梯按钮经验复用

GPT-6 Astra 读取机器人几何、历史图像/动作与可复用局部技能，针对电梯按钮任务生成低层 API 程序；仓库公开仿真与 XLeRobot 真机逐试次数据、代码、报告及演示。

**来源等级：A** · 真机 + 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Sida He, Lingxi Xie, Yunning Cao et al. / Huawei Inc.  
**事件日期：** 2026-09-24（窗口内）  
**日期依据：** Public release commit e324643 dated 2026-09-24T13:31:37+08:00.  
**入口：** [https://github.com/hesd10/astra-robot-sim2real](https://github.com/hesd10/astra-robot-sim2real)  
**代码入口：** [https://github.com/hesd10/astra-robot-sim2real](https://github.com/hesd10/astra-robot-sim2real)  
**许可状态：** 项目整体尚未指定许可；XLeRobot 上游为 Apache-2.0，仓库说明 D3 演示经操作者授权发布。  
**控制接口 / 作用：** 当前相机图像 + 机器人几何/校准 + 历史经验/局部技能 → Astra 生成程序 → 低层仿真或 XLeRobot 控制 API → 新图像反馈

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Synchronized-experience mean-time reduction | 68.6 % | 30 fixed-start simulation trials across 10 conditions | relative to the no-extra-assets/no-experience baseline |
| Simulation-experience real-robot mean-time reduction | 49.9 % | 12 real-robot trials | same-start comparison in the released sim2real study |
| Reusable LOOP skill mean-time reduction | 30.6 % | 27 near-button simulation trials | relative to the condition with no supplied local skill |

**限制与未决项：** 报告的是任务时间相对变化，不是跨任务通用成功率；不同实验组的分母不能合并。 真机成功以操作者确认夹爪尖接触按钮为准，未独立复现。 项目整体无统一许可，不能将公开代码与媒体等同于可自由再分发。 模型权重固定，但经验材料、提示和技能接口随条件改变，指标应按各自协议解释。

paper：[https://github.com/hesd10/astra-robot-sim2real/blob/codex/publication-draft/paper/main.pdf](https://github.com/hesd10/astra-robot-sim2real/blob/codex/publication-draft/paper/main.pdf)  
report：[https://github.com/hesd10/astra-robot-sim2real/blob/codex/publication-draft/report/REPORT.md](https://github.com/hesd10/astra-robot-sim2real/blob/codex/publication-draft/report/REPORT.md)  
video：[https://github.com/hesd10/astra-robot-sim2real/blob/codex/publication-draft/media/D3-realtime-muted.mp4](https://github.com/hesd10/astra-robot-sim2real/blob/codex/publication-draft/media/D3-realtime-muted.mp4)  

**来源：** [S087 · Robot Manipulation with GPT-6-Astra release](SOURCES.md#s087)

---

<a id="p38"></a>
### P38 · From Grasping to Skills · Astra 跨会话技能复用

六次独立 Astra/XLeRobot 牛奶盒抓取会话只通过人工审阅的通用流程与可复用代码跨会话传递经验，记录了成功、失败、恢复与操作者干预。

**来源等级：A** · 真机 · 一手资料明确涉及 GPT-6

**作者 / 团队：** hesd10  
**事件日期：** 2026-09-21（窗口内）  
**日期依据：** Consolidated public release commit 9c12635 dated 2026-09-21T09:43:03+08:00.  
**入口：** [https://github.com/hesd10/astra-grasping-skills](https://github.com/hesd10/astra-grasping-skills)  
**代码入口：** [https://github.com/hesd10/astra-grasping-skills](https://github.com/hesd10/astra-grasping-skills)  
**许可状态：** 仓库未指定项目级许可；公开资料可核验，不据此推定代码或媒体再许可。  
**控制接口 / 作用：** 多相机观察 + 当前会话上下文 + 审阅后的通用 procedure/skill 代码 → Astra 生成与执行机器人程序 → XLeRobot 动作与视觉复核

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Stable-suspension successes | 4 successes | 6 | six successive fresh-workspace/fresh-conversation real-robot carton-grasping attempts |
| Successful-run execution-time reduction | 40.8 % | run 001 (31:39) versus run 006 (18:45) | descriptive sequence comparison; not a controlled causal estimate |

**限制与未决项：** 每个演进版本只有一次尝试，且包含人工干预与第六次前的额外回顾，不能据此建立稳定因果改进。 成功定义为肉眼可见的稳定悬空；要求的 3 cm 间隙没有独立测量。 失败用时是终止前时长，不能与成功用时直接解释为效率。 仓库整体无明确许可，本站只远程引用官方关键帧。

report：[https://github.com/hesd10/astra-grasping-skills/blob/main/physical/report/REPORT.md](https://github.com/hesd10/astra-grasping-skills/blob/main/physical/report/REPORT.md)  
data：[https://github.com/hesd10/astra-grasping-skills/blob/main/results.json](https://github.com/hesd10/astra-grasping-skills/blob/main/results.json)  

**来源：** [S088 · From Grasping to Skills release](SOURCES.md#s088)

---

<a id="p40"></a>
### P40 · Robo-Harness K1 · 感知工具增强机器人智能体

Robo-Harness K1 将标定深度、持久视觉锚点、空间测量与抓取候选暴露为工具；在 18 个配对 LIBERO-PRO case 上，GPT-6 Astra 从 RGB-only 的 11/18 提升到 K1 的 16/18。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Zexi Li, Yehang Zhang, Wenqian Li et al.  
**事件日期：** 2026-09-24（窗口内）  
**日期依据：** arXiv:2609.29389 v1 submitted 2026-09-24T11:16:18Z.  
**入口：** [https://arxiv.org/abs/2609.29389](https://arxiv.org/abs/2609.29389)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 论文为 arXiv non-exclusive distribution license；摘要页未给出公开代码入口。  
**控制接口 / 作用：** RGB/机器人状态 → Astra 选择 grounding、depth、anchor、grasp 等感知工具 → 通用运动/夹爪工具 → 仿真执行与反馈

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| K1 + GPT-6 Astra task accuracy | 88.9 % | 16/18 matched LIBERO-PRO cases | six cases each from Spatial, Object, and Goal; fixed task/state subset |
| RGB-only GPT-6 Astra task accuracy | 61.1 % | 11/18 matched LIBERO-PRO cases | paired task identities and initial states; Inspect Robots RGB-only interface |

**限制与未决项：** Astra 对比只有 18 个预算受限、确定性选取的 case；单个结果会改变 5.6 个百分点。 K1 与 RGB-only 对比同时改变感知、记忆、控制接口和完成反馈，不能把差异归因于单一工具。 Astra 结果来自仿真 LIBERO-PRO；论文跨 embodiment 的 RoboSuite/RoboTwin 迁移使用 Gemini，而非 Astra。 公开摘要未链接代码或独立复现包；结果仅按作者论文记录。

paper：[https://arxiv.org/abs/2609.29389](https://arxiv.org/abs/2609.29389)  
html：[https://arxiv.org/html/2609.29389v1](https://arxiv.org/html/2609.29389v1)  

**来源：** [S090 · Robo-Harness K1 preprint](SOURCES.md#s090)

---

<a id="p41"></a>
### P41 · PyRUA-Lean · 用代码而非逐步工具调用控制机器人

PyRUA-Lean 让 GPT-6 Astra 在持久 Python 命名空间中编写面向 robo 对象的代码，以一次调用组合感知、运动、VLA 技能与状态检查；作者在四组仿真基准上与相同模型、基元和调用预算的 RPent 工具调用方式做配对比较。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Ruiyang Si, Jianxin Bi, Wenbo Huang et al. / DAGroup-PKU  
**事件日期：** 2026-09-25（本月更新，基础项目更早）  
**日期依据：** Repository created 2026-09-25T08:04:11Z; its current canonical public tree is commit 0f88f1c dated 2026-09-26T15:29:24Z after history replacement.  
**入口：** [https://github.com/DAGroup-PKU/PyRUA-Lean](https://github.com/DAGroup-PKU/PyRUA-Lean)  
**代码入口：** [https://github.com/DAGroup-PKU/PyRUA-Lean](https://github.com/DAGroup-PKU/PyRUA-Lean)  
**许可状态：** PyRUA-Lean 采用 Apache-2.0；依赖的 RPent、仿真器、VLA 与模型资产适用各自许可。  
**控制接口 / 作用：** 任务卡/初始图像 + 生成的 robo API 文档 → Astra 编写 Python cells → 沙箱内调用感知、伺服与冻结 VLA 技能 → 同一基准成功判定

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| LIBERO-PRO code-arm success rate | 94.0 % | 40 tasks × 5 seeds; paired against 83.0% tool-calling arm | same GPT-6 Astra, primitives, simulator, success predicate, and 40-response budget |
| RoboTwin 2.0 code-arm success rate | 67.2 % | 50 tasks × 5 buildable seeds; paired against 60.0% tool-calling arm | same model, LingBot-VLA skills, task cells, and request budget |
| RoboCasa365 atomic code-arm success rate | 86.7 % | 18 tasks × 5 seeds; paired against 78.9% tool-calling arm | same model, RLDX-1/navigation skills, task cells, and request budget |
| RoboCasa365 composite code-arm success rate | 39.4 % | 32 tasks × 5 seeds; paired against 34.4% tool-calling arm | same model and 100-response composite-task budget |

**限制与未决项：** 结果由作者提供并附协议与分析脚本，本站未下载模型权重、运行 GPU 仿真或独立复现。 代码臂与工具调用臂的交互形式有意不同：代码臂把多步操作放进 Python cell，工具臂在动作后持续接收图像；结果不能归因为单一低层技能。 成本与 token 降幅仅在两种方式都成功的实例上计算，并依赖发布时的模型价格与网关行为。 四组结果均为仿真；不代表真实机器人成功率。

guide：[https://github.com/DAGroup-PKU/PyRUA-Lean/blob/main/docs/guide.md](https://github.com/DAGroup-PKU/PyRUA-Lean/blob/main/docs/guide.md)  
canonical_commit：[https://github.com/DAGroup-PKU/PyRUA-Lean/commit/0f88f1cc5e3ebacd15869b0697a4739704cdd56c](https://github.com/DAGroup-PKU/PyRUA-Lean/commit/0f88f1cc5e3ebacd15869b0697a4739704cdd56c)  

**来源：** [S093 · PyRUA-Lean official repository](SOURCES.md#s093)

---

<a id="p42"></a>
### P42 · GPT-6 Astra Real2Sim Workflow · 可编辑房间重建与仿真复核

该工作流用 GPT-6 Astra 观察房间照片、决定建模步骤并复查预览，Blender/Python 生成可编辑场景；9 月 30 日又公开同一 Desk1 图像上的原生方案与两条受限 Pi3X/MoGe-3 静态适配对照。

**来源等级：A** · 视觉动画重放 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Roboparty  
**事件日期：** 2026-09-30（本月更新，基础项目更早）  
**日期依据：** Repository first published 2026-09-24; Desk1 comparison release commit f3fedad4 was published 2026-09-30T10:59:47Z.  
**入口：** [https://github.com/Roboparty/gpt-6-astra-real2sim-workflow](https://github.com/Roboparty/gpt-6-astra-real2sim-workflow)  
**代码入口：** [https://github.com/Roboparty/gpt-6-astra-real2sim-workflow](https://github.com/Roboparty/gpt-6-astra-real2sim-workflow)  
**许可状态：** 代码采用 MIT；照片、视频、ArtVIP 参考资产与其他第三方材料按仓库 MEDIA_NOTICE/THIRD_PARTY_NOTICES 分别处理。  
**控制接口 / 作用：** 房间照片 + 已知尺寸/候选家具规格 → Astra 观察、建模决策与预览复查 → Blender/Python 构建 → 几何审计、GLB/USD 导出与可选 MuJoCo 动力学

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| VITBERGET cabinet F-score @10 mm | 59.15 % | 60,000 surface samples per direction against the ArtVIP reference | single reconstructed object; original scale retained; specification/reference assisted |
| BRUKSVARA wardrobe F-score @10 mm | 60.13 % | 60,000 surface samples per direction against the ArtVIP reference | single reconstructed object; original scale retained; specification/reference assisted |
| Independent candidate VITBERGET mean bidirectional surface distance | 25.84 mm | 60,000 samples per direction against the ArtVIP reference | retained 2026-09-26 candidate; rigid alignment only; no scale fit, ICP, or post-measurement revision |
| Independent candidate BRUKSVARA F-score @10 mm | 80.53 % | 60,000 samples per direction against the ArtVIP reference | reference-assisted cabinet metric on the unchanged candidate; not a whole-room score |

**限制与未决项：** 家具规格和 ArtVIP 参考参与制作，评测不是独立留出测试；两个物体的表面指标不能代表整间房间准确率。 新增独立候选的视觉复核要求修改，静态引擎检查因后墙碰撞体偏移 25 mm（容差 6 mm）失败；不能称为仿真就绪。 新旧柜体数值来自不同修订条件；仓库明确说明不能把差异当作控制充分的算法版本比较。 三个 V5 展示场景的大型模型未随 Git 仓库分发；仓库内可复跑案例与展示场景需分开理解。 流程依赖 Astra 进行建模决策，但冻结配方复跑不再调用模型；这不是在线机器人策略。 作者报告 663 个去重几何对象中仍有 77 个开放曲线管件和 2,546 个零面积面。 公开 Space 仅交互预览已有 V5 照片/重建与宣传片，不运行在线重建、接收上传或提供新的实验结果。

video：[https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/main/docs/showcase/media/overview.mp4](https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/main/docs/showcase/media/overview.mp4)  
accuracy：[https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/main/docs/showcase/ACCURACY.md](https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/main/docs/showcase/ACCURACY.md)  
replay：[https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/main/docs/example/REPLAY.md](https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/main/docs/example/REPLAY.md)  
independent_test：[https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/main/examples/independent_whole_scene_20260926/README.md](https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/main/examples/independent_whole_scene_20260926/README.md)  
independent_accuracy：[https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/main/examples/independent_whole_scene_20260926/ACCURACY.md](https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/main/examples/independent_whole_scene_20260926/ACCURACY.md)  
desk1_comparison：[https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/f3fedad4be37a63189edd3414e47095bb3838e2b/docs/research/DESK1_GPT6_PROJECT_COMPARISON_20260930.md](https://github.com/Roboparty/gpt-6-astra-real2sim-workflow/blob/f3fedad4be37a63189edd3414e47095bb3838e2b/docs/research/DESK1_GPT6_PROJECT_COMPARISON_20260930.md)  
project：[https://wgeorge321-roboparty-real2sim-showcase.static.hf.space/index.html](https://wgeorge321-roboparty-real2sim-showcase.static.hf.space/index.html)  
showcase：[https://huggingface.co/spaces/Wgeorge321/roboparty-real2sim-showcase](https://huggingface.co/spaces/Wgeorge321/roboparty-real2sim-showcase)  

**来源：** [S095 · GPT-6 Astra Real2Sim workflow release](SOURCES.md#s095) · [S102 · Astra Real2Sim independent whole-scene audit](SOURCES.md#s102) · [S116 · GPT-6 Astra Real2Sim Desk1 comparison release](SOURCES.md#s116) · [S118 · RoboParty Real2Sim interactive Space showcase](SOURCES.md#s118)

---

<a id="p43"></a>
### P43 · AgenticGenTAMP · 编码智能体合成通用任务与运动规划策略

AgenticGenTAMP 让 Codex（GPT-6 Astra）在 28 个 KinDER/PDDLStream 仿真环境中通过交互探测、编写并调试 Python，最终为每个环境冻结一个可复用策略程序；评测阶段不再调用模型。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Matteo Merler, Bowen Li, Josh Roy et al.  
**事件日期：** 2026-09-24（窗口内）  
**日期依据：** arXiv:2609.30233 v1 submitted 2026-09-24T17:53:35Z; the authors announced the public preprint and project site on 2026-09-25.  
**入口：** [https://agenticgentamp.github.io/](https://agenticgentamp.github.io/)  
**代码入口：** [https://github.com/tomsilver/robocode](https://github.com/tomsilver/robocode)  
**许可状态：** RoboCode 采用 MIT；论文、项目页视频、KinDER/PDDLStream 子模块与第三方仿真资产适用各自许可。  
**控制接口 / 作用：** 任务与状态/动作空间描述 + 隔离仿真器 reset/step/render → Astra 编写、运行并调试 Python → 每个环境冻结一个策略程序 → 100 个留出实例离线评测

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| GPT-6 Astra main-setting mean success | 86 % | 28 simulated environments × 5 synthesis runs × 100 held-out instances | strict black box; no environment source, injected robotics primitives, network, or host filesystem; $20 synthesis budget per run |
| GPT-6 Astra + source mean success | 95 % | 28 simulated environments × 5 synthesis runs × 100 held-out instances | environment source and helper functions available during synthesis; frozen-program evaluation still makes no LLM calls |

**限制与未决项：** 全部结果来自全状态、对象中心的仿真环境；论文明确将感知与语言理解排除在研究范围外，不能外推到真实机器人成功率。 Astra 在合成阶段生成策略代码，而不是在评测阶段逐步在线控制机器人；冻结程序执行时没有模型调用。 论文种子需向作者索取；新种子可复现协议但不保证逐实例复现论文评测集。 结果由作者发布，本站未承担模型调用费用、构建完整仿真依赖或独立复跑 98,000 个评测 episode。

paper：[https://arxiv.org/abs/2609.30233](https://arxiv.org/abs/2609.30233)  
project：[https://agenticgentamp.github.io/](https://agenticgentamp.github.io/)  
code：[https://github.com/tomsilver/robocode](https://github.com/tomsilver/robocode)  
video：[https://agenticgentamp.github.io/assets/project-video.mp4?v=069578f63710](https://agenticgentamp.github.io/assets/project-video.mp4?v=069578f63710)  

**来源：** [S096 · Coding Agents for Generalized Task and Motion Planning Problems preprint](SOURCES.md#s096) · [S097 · AgenticGenTAMP official project page](SOURCES.md#s097) · [S098 · RoboCode official repository](SOURCES.md#s098)

---

<a id="p44"></a>
### P44 · HomeBody · 探索、记忆并执行长程任务的 G1 人形机器人

HomeBody 让 GPT-6 Astra 为 Unitree G1 建立带对象记忆的 Isaac Sim 数字孪生，并通过结构化工具调用编排导航、抓取、放置和开抽屉技能；官网展示它在未见厨房跨房间整理物品，并从含糊请求中取回先前记住的物体。

**来源等级：A** · 真机 + 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Gio Huh, Cayden Gu, Takara E. Truong, C. Karen Liu, Guy Tevet  
**事件日期：** 2026-09-26（窗口内）  
**日期依据：** Official repository created 2026-09-26T02:17:09Z (10:17 Beijing); author X post 2103671433679224912 was published 2026-09-26T02:22:08.771Z (10:22 Beijing).  
**入口：** [https://tml.stanford.edu/homebody/](https://tml.stanford.edu/homebody/)  
**代码入口：** [https://github.com/Stanford-TML/homebody](https://github.com/Stanford-TML/homebody)  
**许可状态：** 仓库尚未声明许可证，README 标注代码即将发布；官网媒体与第三方模型/资产适用各自条款。  
**控制接口 / 作用：** 探索图像、SLAM/关节状态与对象记忆 → Astra 选择目标和结构化技能调用 → 导航、抓取、放置、开抽屉等技能及全身控制器执行 → 结果返回模型

**限制与未决项：** Astra 是高层 VLM/Real2Sim 智能体，并不直接输出高频关节控制；低层运动由导航、操作技能和 AMO 等控制器承担。 官网展示选定的长程任务，但未给出试验次数、成功率分母或完整失败分布，本站未在真实 G1 上独立复现。 项目尚无论文链接，公开仓库标注代码即将发布且未声明许可证；实现与复现实验暂不可完整审计。 作者说明 Astra 推理会在技能之间造成停顿，本地栈需要 RTX 4090 笔记本 GPU，并存在 API 成本和手指过热等部署限制。

project：[https://tml.stanford.edu/homebody/](https://tml.stanford.edu/homebody/)  
code：[https://github.com/Stanford-TML/homebody](https://github.com/Stanford-TML/homebody)  
post：[https://x.com/giohuh_/status/2103671433679224912](https://x.com/giohuh_/status/2103671433679224912)  
teaser：[https://tml.stanford.edu/homebody/videos/teaser.mp4](https://tml.stanford.edu/homebody/videos/teaser.mp4)  

**来源：** [S099 · HomeBody official project page](SOURCES.md#s099) · [S100 · HomeBody official repository](SOURCES.md#s100) · [S101 · Gio Huh HomeBody announcement](SOURCES.md#s101)

---

<a id="p45"></a>
### P45 · R2S2R · Astra 驱动的机器人视角真转仿流程

R2S2R 从机器人外部/腕部相机与关节状态构建 Isaac Lab 场景；其 agentic 路线让 GPT-6 Astra 分阶段选择视图、生成并拟合物体、设定物理参数，再依据仿真重放修正几何。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Qian Wang  
**事件日期：** 2026-09-25（本月更新，基础项目更早）  
**日期依据：** GitHub repository created 2026-09-25T00:17:51Z; quantitative wrist-only PhysCoder results were published in commit 66a5417 on 2026-09-27T21:13:42Z.  
**入口：** [https://github.com/weiqianwang123/R2S2R](https://github.com/weiqianwang123/R2S2R)  
**代码入口：** [https://github.com/weiqianwang123/R2S2R](https://github.com/weiqianwang123/R2S2R)  
**许可状态：** 仓库采用 MIT；SimFoundry、SAM3、Hunyuan3D、FoundationStereo、MuJoCo/Isaac Lab 资产与 DROID 数据适用各自许可。  
**控制接口 / 作用：** 标定 RGB-D/关节轨迹 → Astra 通过受检工具选择帧、分割、生成/拟合网格并组装场景 → Isaac Lab settle/replay → Astra 根据重放复核修正几何

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Agentic wrist-only object centre error | 0.1 cm or less | one synthetic PhysCoder box-block scene | MuJoCo ground-truth capture reconstructed into Isaac Lab; wrist camera only |
| Agentic wrist-only object size error | 0.1 cm or less | one synthetic PhysCoder box-block scene | same author-reported run; compared against simulation ground truth |
| Agentic wrist-only replay depth residual | 1 mm or less | camera frames from the same synthetic run | median absolute depth difference between Isaac Lab replay and recording |

**限制与未决项：** Astra 的量化 agentic 结果来自一个 MuJoCo 合成场景，不是真实 DROID 场景，也不是多任务基准成功率。 仓库同时包含不等同于 Astra 路线的 fixed/SimFoundry 结果；本站未将两条管线的数值合并比较。 流程依赖多套外部模型、GPU 环境、Isaac Lab 与本地 Codex 会话；本站未独立复跑。 重建用于场景生成与重放，不代表 Astra 在线控制真实机器人。

code：[https://github.com/weiqianwang123/R2S2R](https://github.com/weiqianwang123/R2S2R)  
agentic_pipeline：[https://github.com/weiqianwang123/R2S2R/tree/main/src/r2s2r/pipeline/agentic](https://github.com/weiqianwang123/R2S2R/tree/main/src/r2s2r/pipeline/agentic)  
demo：[https://github.com/weiqianwang123/R2S2R/blob/main/docs/demo/ur5e_wrist.gif](https://github.com/weiqianwang123/R2S2R/blob/main/docs/demo/ur5e_wrist.gif)  

**来源：** [S103 · R2S2R official repository](SOURCES.md#s103)

---

<a id="p47"></a>
### P47 · Astra Manipulation · 图像与本体状态驱动的直接仿真控制

Astra Manipulation 让 GPT-6 Astra 根据相机图像、本体状态和动作说明直接输出机械臂或灵巧手的受限数值动作；作者公开了 MuJoCo、PyBullet 与 DexArt/SAPIEN 的逐步轨迹、评测结果和带动作叠层的视频。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** TheShiningVampire  
**事件日期：** 2026-09-28（窗口内）  
**日期依据：** GitHub repository created 2026-09-28T20:39:56Z; reviewed result commit 2792a664 was authored 2026-09-28T22:35:36Z.  
**入口：** [https://github.com/TheShiningVampire/astra-manipulation](https://github.com/TheShiningVampire/astra-manipulation)  
**代码入口：** [https://github.com/TheShiningVampire/astra-manipulation](https://github.com/TheShiningVampire/astra-manipulation)  
**许可状态：** 仓库在本轮检查时未声明许可证；robomimic、Adroit、DexArt/SAPIEN、MuJoCo/PyBullet 数据与依赖适用各自条款。  
**控制接口 / 作用：** 外部/腕部 RGB + 机器人关节、末端或夹爪状态 + 静态执行器说明 → Astra 输出受限姿态增量或原生关节控制及重复步数 → 低层控制器/仿真器执行 → 新观测进入下一轮

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| MuJoCo ten-task pilot completions | 0 successes | 10 | one recorded seed-0 trial per task; 40-decision and 800-control-step ceilings |
| PyBullet reach completions | 3 successes | 3 | three recorded seeds on the simpler Cartesian reach task; different simulator and controller from the MuJoCo suite |
| PyBullet elevated pick-and-place completions | 1 successes | 1 | one recorded trial; selected exploratory evidence, not a success-rate estimate |
| DexArt native-task completions | 0 successes | 4 | one predetermined seen instance each for faucet, laptop, bucket, and toilet under native success checks |

**限制与未决项：** MuJoCo、PyBullet 与 DexArt 的任务、初始状态、控制器和时限不同，不能把结果合并为统一成功率或作受控仿真器比较。 每项只有少量或单次试验；PyBullet 的 3/3 与 1/1 是探索性记录，不能外推为稳定性能。 模型标识记录的是请求的 gpt-6-astra；Codex CLI 事件未暴露服务端解析后的模型标识，本站未重新调用模型核验。 全部结果来自仿真，不代表真机部署；仓库未声明许可证，复用代码或媒体前需取得许可。

code：[https://github.com/TheShiningVampire/astra-manipulation](https://github.com/TheShiningVampire/astra-manipulation)  
ten_task_report：[https://github.com/TheShiningVampire/astra-manipulation/tree/2792a6644c5542ff0db0018320b33a9545e32ef7/reports/ten-task-pilot](https://github.com/TheShiningVampire/astra-manipulation/tree/2792a6644c5542ff0db0018320b33a9545e32ef7/reports/ten-task-pilot)  
dexart_report：[https://github.com/TheShiningVampire/astra-manipulation/tree/2792a6644c5542ff0db0018320b33a9545e32ef7/reports/dexart-pilot](https://github.com/TheShiningVampire/astra-manipulation/tree/2792a6644c5542ff0db0018320b33a9545e32ef7/reports/dexart-pilot)  
video：[https://raw.githubusercontent.com/TheShiningVampire/astra-manipulation/2792a6644c5542ff0db0018320b33a9545e32ef7/reports/bullet-pilot/bullet_pick_place/annotated.mp4](https://raw.githubusercontent.com/TheShiningVampire/astra-manipulation/2792a6644c5542ff0db0018320b33a9545e32ef7/reports/bullet-pilot/bullet_pick_place/annotated.mp4)  

**来源：** [S106 · Astra Manipulation official repository and recorded reports](SOURCES.md#s106)

---

<a id="p48"></a>
### P48 · NavHarness · 跨会话终身具身导航

NavHarness 让 GPT-6 Astra 在连续导航任务间保存地图、任务记录、房屋知识和恢复交接，并在 GOAT-Bench 与 IR2R-CE 中评估跨会话经验复用。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Xunyi Zhao, Jian Zhou, Sihao Lin et al.  
**事件日期：** 2026-09-28（窗口内）  
**日期依据：** arXiv:2609.34276 v1 was submitted 2026-09-28T04:24:47Z.  
**入口：** [https://arxiv.org/abs/2609.34276](https://arxiv.org/abs/2609.34276)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** arXiv v1 以 CC BY 4.0 发布；摘要页未提供公开代码入口。  
**控制接口 / 作用：** RGB 观测 + SLAM 位姿/地图 + 跨任务记录与房屋知识 → GPT-6 Astra 多轮推理与工具调用 → 导航动作、核验与运行总结

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| GOAT-Bench task success | 83.7 % s-SR | GOAT-Bench evaluation | NavHarness with GPT-6 Astra and SLAM-estimated poses; e-SR 36.9% |
| IR2R-CE task success | 85.9 % s-SR | IR2R-CE evaluation | NavHarness with GPT-6 Astra and SLAM-estimated poses |

**限制与未决项：** 结果来自作者论文，本目录未独立复现导航栈或模型调用。 指标依赖 SLAM 估计位姿、基准协议和跨会话记忆设计，不代表无地图真机部署。 摘要页未披露公开代码入口，实验分母与逐场景轨迹需结合论文附录解释。

paper：[https://arxiv.org/abs/2609.34276](https://arxiv.org/abs/2609.34276)  

**来源：** [S108 · NavHarness arXiv paper](SOURCES.md#s108)

---

<a id="p49"></a>
### P49 · CodeActionBench · 具身 Code-as-Policy 评测

CodeActionBench 在 25 项 RoboTwin 2.0 操作任务上要求多模态模型从 RGB 自主估计空间关系、编写并修正机器人程序；GPT-6 Astra 与 Codex CLI 的组合在固定协议下取得最高结果。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Yiheng Lyu, Xueying Jiang, Wenhao Li, Shijian Lu, Gongjie Zhang  
**事件日期：** 2026-09-27（窗口内）  
**日期依据：** arXiv:2609.33807 v1 was submitted 2026-09-27T17:59:31Z.  
**入口：** [https://codeactionbench.org/](https://codeactionbench.org/)  
**代码入口：** [https://github.com/lyhkk/CodeActionBench](https://github.com/lyhkk/CodeActionBench)  
**许可状态：** 论文以 CC BY 4.0 发布；代码仓库许可应在复用前单独核对。  
**控制接口 / 作用：** 多视角 RGB + 标定几何/机器人反馈 API → GPT-6 Astra（Codex CLI）生成并执行 Python 策略 → 受限运动工具与隐藏物理结果核验

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Attempt success rate | 73.3 % | 75 attempts | 25 fixed tasks × 3 attempts; GPT-6 Astra with Codex CLI |
| Task coverage | 22 tasks | 25 | solved at least once in three attempts |

**限制与未决项：** 结果评估的是 GPT-6 Astra 与 Codex CLI 的完整配置，不能只归因于底层模型。 每项任务固定一个场景种子且全部在 SAPIEN/RoboTwin 2.0 仿真中，不代表跨场景泛化或真机成功率。 模型仍使用相机标定、几何计算、运动规划和低层控制 API；并非直接输出关节力矩。

paper：[https://arxiv.org/abs/2609.33807](https://arxiv.org/abs/2609.33807)  
code：[https://github.com/lyhkk/CodeActionBench](https://github.com/lyhkk/CodeActionBench)  
project：[https://codeactionbench.org/](https://codeactionbench.org/)  
video：[https://codeactionbench.org/release-traces/codex-astra/lift_pot/review.mp4](https://codeactionbench.org/release-traces/codex-astra/lift_pot/review.mp4)  

**来源：** [S109 · CodeActionBench paper and project](SOURCES.md#s109)

---

<a id="p50"></a>
### P50 · Astra RoboTwin 2 · 四视角双臂方块堆叠

GPT-6 Astra 从主摄、双腕与固定斜侧相机的 RGB 及机器人自身状态生成受限末端动作，在一个此前三视角阶段中断的 RoboTwin 方块堆叠场景中续跑至官方成功；仓库公开冻结代码、调用记录、审计与录像。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** RedAmancy918  
**事件日期：** 2026-09-28（窗口内）  
**日期依据：** GitHub repository and experiment archive were published in commit d3ca09de on 2026-09-28T10:08:11Z.  
**入口：** [https://github.com/RedAmancy918/astra-robotwin2](https://github.com/RedAmancy918/astra-robotwin2)  
**代码入口：** [https://github.com/RedAmancy918/astra-robotwin2](https://github.com/RedAmancy918/astra-robotwin2)  
**许可状态：** 仓库在本轮检查时未声明许可证；RoboTwin、SAPIEN、CuRobo、模型输出和媒体适用各自条款。  
**控制接口 / 作用：** 四路 RGB + 机器人 TCP/关节/夹爪状态 + 同局交互记忆 → GPT-6 Astra/max → 受限 TCP、XYZ 平移与夹爪动作 → 通用 IK/运动规划 → 官方任务判定

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Four-view continuation completion | 1 successes | 1 | same scene resumed after 72 three-view decisions; 10 new model decisions and 12 new actions; 500/500 post-success physics steps remained successful |

**限制与未决项：** 这是同一中断场景增加第四视角后的续跑，不是独立新测试局，不能解释为总体成功率或第四相机的普遍增益。 原场景累计 82 次模型决策、127 次动作尝试；模型推理时仿真暂停，墙钟时间与物理录像时长不可混用。 运行时隔离不能审计基础模型预训练数据；本站未重新运行模型或仿真。 仓库依赖原实验机环境、外部资产和现有 Codex 登录，不是一键独立复现包。

code：[https://github.com/RedAmancy918/astra-robotwin2](https://github.com/RedAmancy918/astra-robotwin2)  
report：[https://github.com/RedAmancy918/astra-robotwin2/blob/d3ca09de421e09e1fe3bb1a232c2fc4eeb7bc192/runs/20260928-isolated-four-view-resume01/RESULT_REPORT.md](https://github.com/RedAmancy918/astra-robotwin2/blob/d3ca09de421e09e1fe3bb1a232c2fc4eeb7bc192/runs/20260928-isolated-four-view-resume01/RESULT_REPORT.md)  
video：[https://raw.githubusercontent.com/RedAmancy918/astra-robotwin2/d3ca09de421e09e1fe3bb1a232c2fc4eeb7bc192/runs/20260928-isolated-four-view-resume01/videos/agent-seed4885058-0.mp4](https://raw.githubusercontent.com/RedAmancy918/astra-robotwin2/d3ca09de421e09e1fe3bb1a232c2fc4eeb7bc192/runs/20260928-isolated-four-view-resume01/videos/agent-seed4885058-0.mp4)  

**来源：** [S110 · Astra RoboTwin 2 repository and isolated four-view run](SOURCES.md#s110)

---

<a id="p51"></a>
### P51 · RoboHarn-Evo · 从交互中演化层级物理知识

RoboHarn-Evo 不更新基础模型，而是从机器人交互反馈中持续修订任务级与动作级物理知识，并让 GPT-6 在 RMBench 与 RoboDojo 操作任务中检索复用。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Shifeng Bao, Fanding Huang, Yihan Lin et al.  
**事件日期：** 2026-09-29（本月更新，基础项目更早）  
**日期依据：** arXiv:2609.37583 v1 was submitted 2026-09-29T13:42:22Z; v2 followed 2026-09-30T07:12:16Z.  
**入口：** [https://arxiv.org/abs/2609.37583](https://arxiv.org/abs/2609.37583)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 论文为 arXiv non-exclusive distribution license；摘要页未提供公开代码入口。  
**控制接口 / 作用：** 当前场景/目标 + 检索到的任务知识与对象相对动作知识 → GPT-6 分层决策 → 机器人操作 → 物理反馈修订知识库并跨 episode 复用

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| GPT-6 held-out RMBench success after HPK | 88.3 % | held-out RMBench evaluation after 80 interaction rollouts | author-reported increase from 70.0% without the evolved knowledge harness |
| RoboDojo zero-shot transfer gain | 25.0 percentage points | reported GPT-6 transfer evaluation | HPK learned on RMBench and transferred without target-benchmark updates |

**限制与未决项：** 结果来自作者论文，本站未独立运行模型、仿真或知识演化流程。 摘要未完整给出 GPT-6 各指标的 episode 分母与方差；百分比须结合论文协议理解。 提升属于基础模型、检索知识库、执行接口与跨 episode 更新的完整系统，不能只归因于模型。

paper：[https://arxiv.org/abs/2609.37583](https://arxiv.org/abs/2609.37583)  
html：[https://arxiv.org/html/2609.37583v2](https://arxiv.org/html/2609.37583v2)  

**来源：** [S111 · RoboHarn-Evo arXiv paper](SOURCES.md#s111)

---

<a id="p52"></a>
### P52 · RoboChrono · 流式机器人任务理解评测

RoboChrono 用真实机器人执行与徒手人类录像构建 39 个场景、34,713 个实例的流式任务理解基准；GPT-6 Astra 作为零样本对照接受动作识别、视觉对应、时序排序与定位评测。

**来源等级：A** · 非交互评测 · GPT-6 仅作对照

**作者 / 团队：** Yuzhou Wu, Longteng Fan, Zimeng Li et al.  
**事件日期：** 2026-09-29（窗口内）  
**日期依据：** arXiv:2609.36605 v1 was submitted 2026-09-29T03:21:32Z.  
**入口：** [https://arxiv.org/abs/2609.36605](https://arxiv.org/abs/2609.36605)  
**代码入口：** [https://github.com/Continuity3/RoboChrono](https://github.com/Continuity3/RoboChrono)  
**许可状态：** 论文为 arXiv non-exclusive distribution license；代码与数据许可需在复用前分别核对。  
**控制接口 / 作用：** 机器人执行历史与流式视觉片段 → GPT-6 Astra 零样本回答识别、对齐和时序问题；模型不控制机器人

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| GPT-6 Astra Frame Matching accuracy | 98.3 % | RoboChrono Frame Matching evaluation instances | zero-shot evaluation reported by the authors |
| GPT-6 Astra Frame Ordering accuracy | 68.3 % | RoboChrono Frame Ordering evaluation instances | zero-shot evaluation reported by the authors |

**限制与未决项：** Astra 只分析记录的视觉与任务上下文，不向真实机器人输出动作；该卡是评测对照而非控制成果。 98.3% 与 68.3% 属于不同子任务，不能相减解释为统一时序能力下降。 摘要未给出每个 Astra 子任务的精确样本分母；本站未复跑 34,713 个实例。

paper：[https://arxiv.org/abs/2609.36605](https://arxiv.org/abs/2609.36605)  
project：[https://continuity3.github.io/RoboChrono/](https://continuity3.github.io/RoboChrono/)  
code：[https://github.com/Continuity3/RoboChrono](https://github.com/Continuity3/RoboChrono)  

**来源：** [S112 · RoboChrono arXiv paper, project, and repository](SOURCES.md#s112)

---

<a id="p53"></a>
### P53 · LIBERO-Agent · 通用智能体原生机器人操控评测

LIBERO-Agent 让通用智能体自行选择 RGB、深度、标定与机器人状态，并通过原生末端动作操控 MuJoCo 中的 Franka；在 30 项主评测中，GPT-6 Astra 的加权 Performance Score 为 45.0/100，在七个受测智能体配置中最高。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** Zijie Diao, Yitong Chen, Sicheng Xie et al.  
**事件日期：** 2026-09-30（窗口内）  
**日期依据：** arXiv:2609.39507 v1 was submitted 2026-09-30T11:10:10Z; the linked GitHub repository was created earlier that day.  
**入口：** [https://arxiv.org/abs/2609.39507](https://arxiv.org/abs/2609.39507)  
**代码入口：** [https://github.com/dzj441/Libero-Agent](https://github.com/dzj441/Libero-Agent)  
**许可状态：** 论文为 arXiv non-exclusive distribution license；链接仓库声明 MIT，但截至本轮检查仅含代码待发布占位，不能视为完整实现。  
**控制接口 / 作用：** 任务指令 + 可选双视角 RGB/深度、相机标定与机器人状态 → GPT-6 Astra/Codex 自主检查与计算 → 每批 1–50 个受限 OSC_POSE 末端动作 → MuJoCo Franka 与私有任务核验器

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Primary-suite Performance Score | 45.0 /100 | 30 tasks × 3 rollouts | weighted stable score across perception, short-horizon, and long-horizon subsets; GPT-6 Astra with Codex 0.154.0, high reasoning, full observations, and no demonstrations |
| Hard short-horizon stable success rate | 40.0 % | 5 hard short-horizon tasks × 3 rollouts | a task counts only when all three same-seed rollouts succeed |
| Hard long-horizon stable stage completion | 22.0 % | 5 hard long-horizon tasks × 3 rollouts | minimum stage completion across the three rollouts per task |

**限制与未决项：** 结果评估的是 GPT-6 Astra 与 Codex 0.154.0、可用观测、工具和受限控制接口组成的完整配置，不能只归因于基础模型。 全部主评测均为 MuJoCo 仿真，没有真机验证、独立复现或训练数据暴露审计。 45.0 是强调困难长程任务的加权分数，不是原始任务成功率；不同子集指标不可直接混算。 论文链接的 GitHub 仓库当前仅含代码待发布说明，公开代码、任务资产与结果复现条件仍待补齐。

paper：[https://arxiv.org/abs/2609.39507](https://arxiv.org/abs/2609.39507)  
html：[https://arxiv.org/html/2609.39507](https://arxiv.org/html/2609.39507)  
code：[https://github.com/dzj441/Libero-Agent](https://github.com/dzj441/Libero-Agent)  

**来源：** [S117 · LIBERO-Agent arXiv paper and linked repository](SOURCES.md#s117)

---

## 配套资源与对照 · 10

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

**限制与未决项：** 框架本体不算新的独立 GPT-6 成功案例。 默认安全检查不构成硬件安全认证。 v0.59.0 增加环境预算提示、provenance、Jev/AprilTag 支持及验证/日志修复。

release：[https://github.com/robocurve/inspect-robots/releases/tag/v0.59.0](https://github.com/robocurve/inspect-robots/releases/tag/v0.59.0)  

**来源：** [S026 · Inspect Robots](SOURCES.md#s026) · [S079 · Inspect Robots v0.59.0](SOURCES.md#s079)

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

**限制与未决项：** 09-16/17 更新涉及 observation 时序、RGB byte order 与 swap_T 资产，应固定代码和数据版本。 不要直接混用旧评测快照与新资产。 商业使用前必须解决许可文本不一致。 2026-09-19 修正 organize_table 任务说明；没有新增评测结果。

task_update：[https://github.com/robodojo-benchmark/RoboDojo/commit/726e9aabfaa642203722eb126f5eaf0f37f3e1ad](https://github.com/robodojo-benchmark/RoboDojo/commit/726e9aabfaa642203722eb126f5eaf0f37f3e1ad)  

**来源：** [S016 · RoboDojo official code](SOURCES.md#s016) · [S017 · RoboDojo project site](SOURCES.md#s017) · [S080 · RoboDojo organize_table task correction](SOURCES.md#s080)

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

<a id="p25"></a>
### P25 · Robot Agent Gallery · Astra 仿真机器人评测画廊

汇总 Astra 从 RGB 与本体状态在线控制 LIBERO、RoboTwin、RoboCasa365、RoboDojo 等仿真基准的公开结果和可播放 episode。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** tianqi-zh  
**事件日期：** 2026-09-18（窗口内）  
**日期依据：** GitHub repository created 2026-09-18; Robotwin media/results were refreshed on 2026-09-22.  
**入口：** [https://github.com/tianqi-zh/robot-agent-gallery](https://github.com/tianqi-zh/robot-agent-gallery)  
**代码入口：** [https://github.com/tianqi-zh/robot-agent-gallery](https://github.com/tianqi-zh/robot-agent-gallery)  
**许可状态：** 仓库未见统一媒体再许可；本地仅保留仓库社交预览图用于审核。  
**控制接口 / 作用：** RGB + 本体状态 → Astra 动作 → 多仿真基准环境

**限制与未决项：** 各基准任务、控制接口和预算不同，不能合并为单一成功率。 当前画廊计数会随仓库更新，预览记录的是本轮核对状态。 未审计生成这些结果的全部私有源材料。

project：[https://tianqi-zh.github.io/robot-agent-gallery/](https://tianqi-zh.github.io/robot-agent-gallery/)  

**来源：** [S067 · Robot Agent Gallery repository and media](SOURCES.md#s067)

---

<a id="p27"></a>
### P27 · LLM Robotics Playground · 五项仿真机器人实验

Astra/Codex 协助搭建四项 MuJoCo 环境和控制器；2026-09-24 新增 Baoding balls Isaac Lab/PhysX PPO 基线、checkpoint 与固定回放，该新增项本身不使用 Astra 在线控制。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** dimentary  
**事件日期：** 2026-09-17（窗口内）  
**日期依据：** Repository and v0.1.0 release both published 2026-09-17.  
**入口：** [https://github.com/dimentary/llm-robotics-playground](https://github.com/dimentary/llm-robotics-playground)  
**代码入口：** [https://github.com/dimentary/llm-robotics-playground](https://github.com/dimentary/llm-robotics-playground)  
**许可状态：** 项目代码 MIT；上游机器人模型及鸽子图样保持各自许可。  
**控制接口 / 作用：** 前四项：Astra/Codex 编写环境与控制代码 → 仿真真值状态/接触 → 固定控制器回放；Baoding：PPO 训练策略 → Isaac Lab/PhysX rollout → MuJoCo 运动学回放

**限制与未决项：** 不是 Astra 在线闭环控制。 项目样例不能作为通用机器人成功率。 上游资产许可应与 MIT 代码分开理解。 Baoding balls 是独立 RL 基线，不能归因于 GPT-6 Astra。

release：[https://github.com/dimentary/llm-robotics-playground/releases/tag/v0.1.0](https://github.com/dimentary/llm-robotics-playground/releases/tag/v0.1.0)  

**来源：** [S069 · LLM Robotics Playground repository](SOURCES.md#s069)

---

<a id="p32"></a>
### P32 · 当地图成为程序 · Astra World Model

Astra 读取 RGB/几何输入并调用 Blender 构造对象化三维场景；下游用生成场景做无人机复拍和 G1 语言导航。

**来源等级：A** · 仿真 · 一手资料明确涉及 GPT-6

**作者 / 团队：** wentingw  
**事件日期：** 2026-09-23（窗口内）  
**日期依据：** GitHub repository created 2026-09-23 UTC.  
**入口：** [https://github.com/wentingw/astra-world-model-blog](https://github.com/wentingw/astra-world-model-blog)  
**代码入口：** [https://github.com/wentingw/astra-world-model-blog](https://github.com/wentingw/astra-world-model-blog)  
**许可状态：** 仓库研究资产未见统一再许可声明；本地仅保留官方 hero 图。  
**控制接口 / 作用：** RGB/几何输入 → Astra + Blender 工具 → 对象化 3D 场景 → 下游固定控制器

| 指标 | 结果 | 分母 | 协议 / 注意事项 |
| --- | --- | --- | --- |
| Drone exact revisit | 0 successes | 20 | M3 generated-scene downstream evaluation |
| G1 language-navigation arrival | 18 successes | 30 | declared model-world evaluation |

**限制与未决项：** 不是 Astra 在线控制无人机或 G1。 无人机准确复拍 0/20；G1 的 18/30 只适用于声明的模型世界。 冻结资产与机器可读结果仍是作者自报。


**来源：** [S074 · Astra World Model research repository](SOURCES.md#s074)

---

<a id="p39"></a>
### P39 · BluPe Remote YAM · Astra 共享真机运行基础设施

开源 runner 让本地 Codex/Astra 通过公开 Session API 加入 BluPe 共享 YAM/SO101 机器人队列，读取三路相机并提交受限轨迹；近期更新加入运行对比指标与可选推理强度。

**来源等级：A** · 真机 + 仿真 · 基础设施，不是单独的 GPT-6 成果

**作者 / 团队：** Andrew Liu / BluPe  
**事件日期：** 2026-09-07（本月更新，基础项目更早）  
**日期依据：** GitHub repository created 2026-09-07T08:32:16Z; active run-metrics and reasoning-effort updates landed 2026-09-25.  
**入口：** [https://github.com/andlyu/blupe-remote-yam](https://github.com/andlyu/blupe-remote-yam)  
**代码入口：** [https://github.com/andlyu/blupe-remote-yam](https://github.com/andlyu/blupe-remote-yam)  
**许可状态：** 仓库无统一项目许可；RoboCurve 适配代码与 I2RT/robot models 各自保留上游许可。  
**控制接口 / 作用：** 远端三相机/队列状态 → 本地 Astra runner 与 IK → Session API 轨迹请求 → 网关就绪/限位/停止检查 → 共享 YAM 或 SO101

**限制与未决项：** 这是可复用基础设施，不是独立 GPT-6 成功率或新模型能力结果。 真机执行依赖共享队列、现场操作者就绪和网关安全检查；本轮未远程启动机器人。 仓库未提供统一许可，不能把可访问性等同于可自由再分发。 mock 与 no-hardware-control 模式不构成真机验证。

runs：[https://huggingface.co/datasets/andlyu/Public-YAM-runs](https://huggingface.co/datasets/andlyu/Public-YAM-runs)  
api：[https://github.com/andlyu/blupe-remote-yam/blob/main/API.md](https://github.com/andlyu/blupe-remote-yam/blob/main/API.md)  

**来源：** [S089 · BluPe Remote YAM runner](SOURCES.md#s089)

---

<a id="p46"></a>
### P46 · RC DexBench · GPT-6 Astra 灵巧手评测接口

RC DexBench 为按键、钢琴序列和固定场景抓放定义事件级评分与统一适配器；示例策略通过 GPT-6 Astra 每轮选择一个受限手指动作，但公开快速示例只连接 mock adapter。

**来源等级：A** · 仿真 · 基础设施，不是单独的 GPT-6 成果

**作者 / 团队：** Robotics Center  
**事件日期：** 2026-09-28（窗口内）  
**日期依据：** GitHub repository created 2026-09-28T00:42:19Z; public README/media/Astra example were completed in commit 89599c3 at 2026-09-28T00:58:24Z.  
**入口：** [https://github.com/RoboticsCenter/dexbench](https://github.com/RoboticsCenter/dexbench)  
**代码入口：** [https://github.com/RoboticsCenter/dexbench](https://github.com/RoboticsCenter/dexbench)  
**许可状态：** 仓库采用 Apache-2.0；连接的机器人、数据记录、模型服务与第三方资产适用各自许可。  
**控制接口 / 作用：** 任务/观测 → Astra 从 index/middle/ring/stop 中选择单个受限动作 → adapter 映射到手指运动 → 键盘、MIDI、触觉与时钟事件记录和评分

**限制与未决项：** 公开 README 的 Astra 命令使用 mock adapter；没有发布 GPT-6 Astra 真机成功率、结果文件或 MCAP 试验集。 任务 GIF 与真实夹爪照片用于说明基准硬件和协议，不证明模型已在这些设备上完成评测。 替换为真实机器人 adapter 需要维护者自行实现硬件映射、校准与安全边界。 这是新发布的评测基础设施，不是独立的 GPT-6 机器人能力结果；本站未调用模型或硬件。

code：[https://github.com/RoboticsCenter/dexbench](https://github.com/RoboticsCenter/dexbench)  
spec：[https://github.com/RoboticsCenter/dexbench/blob/main/SPEC.md](https://github.com/RoboticsCenter/dexbench/blob/main/SPEC.md)  
adapter_guide：[https://github.com/RoboticsCenter/dexbench/blob/main/docs/add_an_adapter.md](https://github.com/RoboticsCenter/dexbench/blob/main/docs/add_an_adapter.md)  

**来源：** [S104 · RC DexBench official repository](SOURCES.md#s104)

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

作者原帖明确称 GPT-6 Astra 用机器人手解开魔方；个人演示页确认对应项目运行于 MuJoCo 双手仿真。

**来源等级：C** · 仿真 · 作者声明，经镜像获取

**作者 / 团队：** @ZeYanjie  
**事件日期：** 2026-09-10（窗口内）  
**日期依据：** 原帖 status ID 2098118164626501669 的 X Snowflake 时间为 2026-09-10T18:35:26Z  
**入口：** [https://x.com/ZeYanjie/status/2098118164626501669](https://x.com/ZeYanjie/status/2098118164626501669)  
**代码入口：** 未定位公开代码；不等于确认代码不存在  
**许可状态：** 未核实  
**控制接口 / 作用：** 未披露/未核实

**限制与未决项：** 完整控制方式与在线/离线搜索协议未核实，不直接标“真机零样本”。 原帖正文已由公开嵌入接口核对，但提示、完整日志与代码均未公开；未独立复现。

post：[https://x.com/ZeYanjie/status/2098118164626501669](https://x.com/ZeYanjie/status/2098118164626501669)  
demo：[https://dex-rubik-cube.yanjieze.com/](https://dex-rubik-cube.yanjieze.com/)  

**来源：** [S040 · Yanjie Ze project directory](SOURCES.md#s040) · [S041 · Dex Rubik GPT6 author post, mirror](SOURCES.md#s041) · [S105 · ZeYanjie Rubik's Cube original X post](SOURCES.md#s105)

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
