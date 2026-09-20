# 每日发现与人工审核队列

`scripts/daily_review.py` 生成不可发布的审核材料，不修改正式数据，不分配正式 ID，也不提交、推送、开 PR 或发布。网络读取默认关闭；fixture 测试和日常单元测试完全离线。

## 本地演练

```bash
python3 scripts/daily_review.py --dry-run
python3 scripts/daily_review.py --once \
  --fixture tests/fixtures/daily_review_items.json \
  --from 2026-09-01T00:00:00Z --to 2026-09-20T00:00:00Z
```

审核包写入 `.gitignore` 已覆盖的 `downloads/daily-review/<UTC日期>/<run_id>/`，状态索引写入独立的 `downloads/daily-review-state/state.json`。包内含 `run.json`、候选/证据/决策 JSONL、post 下载清单、保留用户原名的媒体映射表、报告和 `SHA256SUMS`。正式文件在运行前后均计算 SHA-256；不一致则运行失败。

启用公开网络读取必须显式增加 `--network`。采集器支持以下配置驱动的公开入口；`config/daily_review.example.json` 给出可直接替换占位符的示例，默认配置不含查询目标，因而不会联网：

- `github_searches` 使用 GitHub 公开 repository search，查询词真实进入 `q`；命中仍是 search lead，保持 `needs_evidence`。`github_repositories` 读取公开 repository、releases、窗口内 commits，入口指向原始仓库。
- `feeds` 解析 RSS 2.0/Atom。若 entry 正文链接具体 X status/小红书 note，则创建具体 post 候选并保留 feed 入口；否则只保留 `needs_evidence` lead。
- `discovery_indexes` 从公开 HTML 索引抽取具体 post 链接；仅主页/title 或无法追到原始入口时仍为 `needs_evidence`，不冒充原帖发现。
- `arxiv_queries` 查询模板必须同时包含 `{model_terms}` 和 `{embodied_terms}`。适配器按 `lastUpdatedDate` 降序读取、以 Atom entry 的 `updated` 本地筛选冻结窗口，再核对模型词与具身词；因此首版早于 lower bound、但修订发生在窗口内的论文不会被 `submittedDate` 错误排除。

`--response-fixture` 可让 GitHub JSON、RSS/Atom 与 arXiv Atom 的真实响应格式完全离线走同一解析路径。

每个适配器/查询独立计算窗口和记录完成状态。arXiv 官方手册说明 `start/max_results` 是 offset 分页、`published` 是首版提交、`updated` 是当前版本更新时间，并提供 `lastUpdatedDate` 排序；它不承诺多次请求之间的结果集快照。故部分分页会写入 `pagination_incomplete_unstable_offset_restart_required`，冻结时间窗但下一次从第 0 页完整重扫，绝不从旧 offset 静默“续完”。GitHub search 的动态排名采用同样原则；`incomplete_results=true`、超过 1000 条的 API 上限、total 未满足却出现空页、total 跨页变化或无效条目都会失败留证。feed 登录页、非 RSS/Atom 根节点与无效 entry URL 也失败；缺失/不可解析日期则保留为 `unknown` 候选证据。只有一次运行完整分页、输入有效、审核包及状态事务均成功时才推进水位。参考：[arXiv API User's Manual](https://info.arxiv.org/help/api/user-manual.html)。

所有真实 HTTP 请求共用限速器并执行 `minimum_request_interval_seconds`。初始 URL 在请求前检查 allowlist/denylist；自定义 redirect handler 在跟随每一跳之前检查目标，最终 URL 再复核后才读取/接受正文。HTTP 401/403/429 保留状态码，证据 URL 删除凭据、签名和 tracking 参数。不登录、不使用 cookie、不绕过 CAPTCHA/付费墙，也不会自动调用社媒下载器。

配置 seed 页目前只提取 HTML title，并保存该候选专属页面的内容哈希作为“页面变化、需复审”信号；它不解析正文事实，也不能声称完成了原始链接追踪。arXiv 条目使用单条 entry 的稳定结构哈希，避免整页分页哈希使无关候选变化。每次有效观察都会写 evidence；新增第二来源会关联既有候选，已知来源内容变化则创建独立更新版本。

## 审核与恢复

- `candidates.jsonl` 是机器候选，不是正式条目。中英文标题和摘要均带 `machine_generated_not_source_text` 标记。
- `decisions.jsonl` 初始为空。人工审核将决定追加到独立 JSONL 后，可在下一次运行用 `--decisions <path>` 合并；采集器校验候选 ID、最终状态、审核人、时间和理由，将事件原样带入新审核包，并且不会把最终状态降回自动状态。
- approved 事件只生成 `change-plans.jsonl` / `change-plan.md`：仅采用 `accepted_fields` 明确列出的字段；空数组表示不采用任何字段，与 `rejected_fields` 有交集则拒绝整条决定。日期迁移必须同时明确接受 `event_date` 与 `event_date_basis` 且候选含日期依据，否则正式窗口保持不变并标记 pending。它不修改正式文件、不分配正式 ID。
- `--user-media-map <csv>` 接收 `candidate_id,user_supplied_path,original_filename`。候选必须是已知具体 post，原名必须与上传文件 basename 完全一致；审核包使用 `media-staging/<candidate>/<hash-prefix>/<original-name>` 保留原件与原名，允许同一候选同名不同内容且对同内容去重。每条映射均记录 SHA-256，复制后再次校验。正式建议严格采用现有 `assets/social/<编码原名>` 单文件结构；同名不同内容或与既有正式媒体内容冲突时留空建议并标记 `needs_manual_path_resolution`，不静默改名或扩展正式 schema。
- `--from`、`--to` 使用带时区的 ISO-8601；默认首次回看 30 天，后续分别从各适配器成功水位减 72 小时。历史补跑不会使任何水位倒退。
- identity 保存不可变候选版本。版本身份由完整事实 snapshot 与可用的稳定 evidence source/hash 共同确定；任何追加前先查全部历史版本，并拒绝 candidate ID 碰撞。相同版本只更新观察时间、不重复入队；变化内容生成新的候选 ID、字段 diff、`update_of` 和关联旧 decision，不覆盖旧版本。事实 A→B→A 或固定事实下证据 hash A→B→C→B 的复现只追加 `reappearances` 并把证据关联回原版本，不重复创建 ID，也不遮盖原人工决定。
- 包发布和状态更新采用检查点事务。`--resume-run <id>` 可完成 `package_ready/package_published` 提交；进程在 collecting 阶段崩溃时，残留暂存区移入 `state/abandoned/` 留证，并用原参数和相同 run ID 从头安全重跑。
- 状态含单调 `revision` 和 `committed_runs`。检查点记录 `base_revision`；旧事务若与新状态/人工决定交错会标记 `stale_conflict` 并拒绝覆盖，重复提交则按 run ID 幂等识别。启动新 run 前必须先恢复或处置遗留事务。collecting/restart_pending 重跑固定原 upper bound、逐适配器窗口、cursor 和配置哈希。
- `--adapter fixture|seed|arxiv|github|feed` 可限制补跑。状态只在取得单实例锁后读取；锁冲突返回码 75 和 `skipped_locked`。
- SIGINT/SIGTERM 设置停止标志，不再领取候选，生成 `interrupted` 审核包；未完成适配器不推进水位。
- 输出和状态目录必须位于仓库 `downloads/` 下；run ID 只接受有限安全字符，禁止路径穿越。

## 部署边界与停止

默认配置明确为 `persistence.configured=false`，所以当前能力只是本地 `--once` 演练，**没有每日任务已启用**。正式调度前必须另行决定持久卷/对象存储/数据库、条件写或单写者策略、审核包 artifact 保留期、secret 注入方式，以及 Asia/Taipei 02:30 的调度器配置。临时 CI runner 的 `downloads/` 不能作为持久化方案。

当前未实现：Hugging Face API、付费/受限社媒搜索 API、项目官方媒体自动下载、可直接应用的正式补丁，以及外部持久化/artifact 上传。`project_pages`、`huggingface_seeds`、`social_post_seeds` 仍是保守单页 seed 检查；它们不能替代正文事实提取或全网搜索。GitHub、feed 和 arXiv 仅完成离线 fixture 验证，尚未做公网端到端验证，也未配置任何凭据或部署。

停止已部署任务应禁用外部 scheduler；本仓库没有安装、启动或杀死任何后台进程。

候选字段和状态语义见 [DAILY_REVIEW_SCHEMA.md](DAILY_REVIEW_SCHEMA.md)。
