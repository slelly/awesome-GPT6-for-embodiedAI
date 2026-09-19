# Hugging Face 资源地图

这 8 个资源与主目录交叉关联，**不是另外 8 个独立 GPT-6 实验，也不包含 GPT-6 的开放权重**。

模型适配器、演示数据、评测轨迹、基准资产必须分开；旧版快照不能与新版相加。许可按对应版本的文件核对。

| ID | 资源 | 类型 | 对应项目 | 核验范围 |
| --- | --- | --- | --- |
| HF01 | [AGP canonical evaluated trials](https://huggingface.co/datasets/Agent-as-Policy/agent-as-policy) | dataset | [P03](CATALOG.md#p03) | primary_card |
| HF02 | [AGP earlier YAM snapshot](https://huggingface.co/datasets/Agent-as-Policy/yam-agent-as-policy) | dataset | [P03](CATALOG.md#p03) | legacy_snapshot |
| HF03 | [Astra RoboDojo rollouts](https://huggingface.co/datasets/YuMoool/astra-robodojo-rollouts) | dataset | [P02](CATALOG.md#p02) | primary_card |
| HF04 | [Show-Harness VLM adapters](https://huggingface.co/showlab/Show-Harness-VLMs) | model_adapter | [P14](CATALOG.md#p14) | primary_card |
| HF05 | [Show-Harness demonstrations](https://huggingface.co/datasets/showlab/Show-Harness-Data) | dataset | [P14](CATALOG.md#p14) | primary_card |
| HF06 | [PhysBrain 1.5 8B](https://huggingface.co/DeepCybo/PhysBrain1.5-8B) | model | [P15](CATALOG.md#p15) | linked_from_primary |
| HF07 | [PhysBrain 1.5 2B](https://huggingface.co/DeepCybo/PhysBrain1.5-2B) | model | [P15](CATALOG.md#p15) | linked_from_primary |
| HF08 | [RoboDojo official HF repository](https://huggingface.co/datasets/RoboDojo-Benchmark/RoboDojo) | dataset | [P16](CATALOG.md#p16) | partial_index |

## HF01 · AGP canonical evaluated trials

162 evaluated rows，多模型；适合轨迹和工具调用研究。

许可：CC BY 4.0

来源：[S006](SOURCES.md#s006) · [S007](SOURCES.md#s007)

## HF02 · AGP earlier YAM snapshot

旧卡为 196 sessions，含 reset/auxiliary；不与 HF01 合并计数。

许可：CC BY 4.0

来源：[S008](SOURCES.md#s008)

## HF03 · Astra RoboDojo rollouts

100 rows = 50 cases ×2 methods；全量列表约 135 GB，先选读 metadata/core records。

许可：数据 CC BY 4.0；reader code 见原 LICENSE

来源：[S045](SOURCES.md#s045)

## HF04 · Show-Harness VLM adapters

五个真实机器人 adapter 与一个仿真 adapter；不是 GPT6 权重。

许可：Qwen: Apache-2.0；Gemma: Gemma terms

来源：[S028](SOURCES.md#s028)

## HF05 · Show-Harness demonstrations

164 real +230 sim episodes；支持语义动作控制研究，不标记 GPT6 专属数据。

许可：Apache-2.0

来源：[S029](SOURCES.md#s029)

## HF06 · PhysBrain 1.5 8B

独立开源基模；链接由项目 README 确认，模型卡未单独完整取得。

许可：未核实

来源：[S031](SOURCES.md#s031)

## HF07 · PhysBrain 1.5 2B

同系列小模型；与 GPT6 的关系仅为相关研究/比较，不是 GPT6 发布。

许可：未核实

来源：[S031](SOURCES.md#s031)

## HF08 · RoboDojo official HF repository

仓库存在的 PR 文件索引已见；main 资源完整性/版本/许可应从官方文档再次核实。

许可：未核实

来源：[S016](SOURCES.md#s016) · [S046](SOURCES.md#s046)

## 下载之前

先看文件树、许可证、版本和容量，再下载所需清单或单个案例。评测数据与真实机器人轨迹可能包含人的语音、图像或现场信息，不应默认允许再发布。

YuMoool 的完整回放包约 135 GB；只读结果不需要模拟器。AGP 的 canonical 卡与旧 YAM 卡采用不同统计口径；不把 reset/auxiliary sessions 计作 evaluated trials。来源：[S045](SOURCES.md#s045)、[S006](SOURCES.md#s006)、[S008](SOURCES.md#s008)。

本仓库没有下载这些大文件、替用户接受访问协议或执行远程数据中的脚本。访问错误、revision 和依赖版本应在实际使用时重新确认。
