# Gallery tags

Cards combine one or two factual scene tags (`simulation` / `real world`) with one or more workflow tags. Tags are additive: they help visitors search and compare work; they do not claim a shared benchmark, deployment result, or model capability.

| Tag | English | 中文 | Applied from category |
| --- | --- | --- | --- |
| `sim` | simulation | 仿真 | scene tag |
| `real` | real world | 真机 | scene tag |
| `control` | control | 控制 | closed_loop, hybrid, policy_improvement, harness, hierarchical_control, dexterous_sim, paused_physics, generated_control, planned_replay |
| `evaluation` | evaluation | 评测 | evaluation, coding_evaluation |
| `policy` | policy | 策略 | hybrid, policy_improvement |
| `real-to-sim` | real-to-sim | 真转仿 | real2sim |
| `replay` | replay | 重放 | real2sim, planned_replay |
| `code-generation` | code generation | 代码生成 | coding_evaluation, generated_control |
| `harness` | harness | 测试框架 | harness |
| `benchmark` | benchmark | 基准 | understanding_benchmark, benchmark, discovery_collection |
| `understanding` | embodied understanding | 具身理解 | understanding_benchmark |
| `dexterous` | dexterous manipulation | 灵巧操作 | dexterous_sim, rl_engineering |
| `rl-training` | RL training | 强化学习训练 | rl_engineering, environment_engineering |
| `physics` | physics simulation | 物理仿真 | paused_physics |
| `environment-building` | environment building | 环境构建 | environment_engineering |

## Project mapping

| ID | Scene tags | Workflow tags |
| --- | --- | --- |
| P01 | real | control |
| P02 | sim | control, policy |
| P03 | real | control |
| P04 | real | evaluation |
| P05 | real | evaluation |
| P06 | sim, real | evaluation |
| P07 | real | policy, control |
| P08 | sim | real-to-sim, replay |
| P09 | sim | real-to-sim, replay |
| P10 | sim | real-to-sim, replay |
| P11 | sim | real-to-sim, replay |
| P12 | real | evaluation, code-generation |
| P13 | sim, real | harness, control |
| P14 | sim, real | harness, control |
| P15 | sim, real | benchmark, understanding |
| P16 | sim, real | benchmark |
| P17 | sim | benchmark |
| P18 | real | evaluation |
| P19 | real | control |
| P20 | sim | evaluation, code-generation |
| P21 | sim | code-generation, control |
| P22 | sim | code-generation, control |
| P23 | sim | control |
| P24 | real | evaluation |
| P25 | sim | evaluation |
| P26 | real | control, policy |
| P27 | sim | code-generation, control |
| P28 | sim | code-generation, control |
| P29 | sim | control |
| P30 | sim | control |
| P31 | sim | control |
| P32 | sim | environment-building, rl-training |
| P33 | sim | control, policy |
| P34 | real | harness, control |
| P35 | sim, real | control |
| P36 | real | evaluation |
| P37 | sim, real | policy, control |
| P38 | real | policy, control |
| P39 | sim, real | harness, control |
| P40 | sim | harness, control |
| P41 | sim | harness, control |
| P42 | sim | real-to-sim, replay |
| X01 | real | control |
| X02 | real | control |
| X03 | real | control |
| X04 | real | control |
| X05 | sim | control |
| X06 | sim | control |
| X07 | sim | dexterous, control |
| X08 | sim | rl-training, dexterous |
| X09 | sim | physics, control |
| X10 | sim | control |
| X11 | sim | code-generation, control |
| X12 | sim | code-generation, control |
| X13 | sim | replay, control |
| X14 | sim | environment-building, rl-training |
| X15 | real | control |
