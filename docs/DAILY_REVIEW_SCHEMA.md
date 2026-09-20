# 候选审核数据契约

审核队列不是正式 `data/projects.json` schema。候选 ID 形如 `C-<16位哈希>`，由规范 identity 与该次内容 fingerprint 共同派生；同一 identity 的内容变化会得到新的不可变版本，不会占用 `Pxx`、`Xxx` 或 `Rxx`。

## `candidates.jsonl`

每行包含 identity（`candidate_id`、`candidate_kind`、`canonical_key`、`content_fingerprint`）、观察时间与 `status`、中英文机器草案、入口 URL、作者、拟议 section/category/environment/scene tags、派生 workflow tags、GPT-6 关系与证据级别、日期及解析依据、许可/接口/指标/限制、事实与推断分离字段、证据/媒体引用、重复或更新关系、差异字段、taxonomy 请求和审核备注。

自动状态仅为 `new`、`needs_evidence`、`needs_user_media`、`possible_duplicate`、`possible_update`、`ready_for_review`。`approved`、`rejected`、`superseded` 只能来自人工追加决策。相同版本只更新观察索引、不再次进入审核包；新证据导致 fingerprint 变化时建立独立 `possible_update` 版本，通过 `update_of` 和 `related_decision` 回指旧版本，不覆盖旧决定。版本身份包含事实 snapshot 与可用的 evidence source/hash；追加前查找全部历史身份并防御 candidate ID 重复。A→B→A 和 evidence hash A→B→C→B 的复现都写入 `reappearances` 并让 evidence 回指原版本，不再次插入同 ID 或覆盖其 decision。

## `evidence.jsonl`

每条记录稳定 evidence ID、候选 ID、来源/规范/final URL、来源类型、访问方式、抓取时间、HTTP 与解析状态、内容哈希、提取器版本、最小事实摘要、日期/媒体/许可说明和失败原因。不保存整篇受版权保护正文，不保留 token、cookie 或签名 query。

每次有效观察都写 evidence，即使候选事实 fingerprint 未改变。identity 另存按稳定来源键索引的证据观察；相同来源的候选专属内容哈希变化产生 `evidence_content:<source>` 更新，新来源则关联当前候选但不伪造事实变化。重定向原 URL 和最终 URL 注册为 aliases，用于跨日 identity 去重。

## `decisions.jsonl`

人工系统按追加写记录 `candidate_id`、`decision`、`reviewer`、`decided_at`、理由、采用或拒绝字段、媒体决定、关联正式 ID 和基线 SHA。采集器创建空文件但不代替人工决策。

approved 只触发审核包内的 `change-plans.jsonl` / `change-plan.md`。计划只采用 `accepted_fields` 明确列出的字段；空数组不代表全字段，采用/拒绝字段交集为非法。只有 `event_date` 与 `event_date_basis` 都明确获准且候选有日期依据时才派生窗口迁移，否则窗口保持不变、状态为 `pending_unapproved_or_unverified_date`。`proposal_only=true`、`formal_id_assigned=false` 是强制边界。

## 用户媒体映射

`--user-media-map` CSV 的必填列为 `candidate_id`、`user_supplied_path`，可显式提供 `original_filename`，但它必须与文件 basename 完全一致。输出 `media-name-map.csv` 为每个输入保留一行；原件复制到 `media-staging/<candidate_id>/<sha256-prefix>/<original_filename>`，复制后重新核对 SHA-256。相同内容可复用包内文件，同名不同内容由 hash 目录隔离，不同候选由 candidate 目录隔离。正式 URL 建议必须保持当前 `assets/social/<percent-encoded-original-filename>` 三段结构；同名不同内容或与既有正式文件内容冲突时 `suggested_site_path` 留空、`mapping_status=needs_manual_path_resolution`，由人工决定，不暗改原名或 schema。只接受已有具体 post 候选，不自动下载、不写 `data/media.json`。

## Identity 与更新

- GitHub：小写 `owner/repo`，忽略 `.git`、query、fragment。
- arXiv/DOI：规范 ID；arXiv 新式及旧式分类 ID 均去除 `vN` 版本后缀。
- 社媒：平台加具体 post/status ID；主页不是帖子 identity。
- 其他 HTTPS：主机小写但保留路径大小写及有语义 query；去除 fragment、tracking、凭据与签名参数。
- fingerprint 使用标题、作者、入口、日期、拟议分类、关系事实和媒体哈希的确定性 JSON。

与正式数据 identity 相同为 `possible_duplicate`；明确提供变更或历史 fingerprint 改变为 `possible_update`。未知事实保持 `null`/`unknown`，不得以抓取日冒充事件日。
