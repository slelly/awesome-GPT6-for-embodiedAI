# 贡献指南

欢迎补充项目、原始 X / 小红书链接、公开代码、失败案例、协议与数据；也欢迎降级被过度解读的条目。

## 添加或修正

先在 `data/projects.json` 检查同一项目的别名。新项目使用唯一 ID；来源写入 `data/sources.json` 并用 `source_ids` 关联。每条必须包含环境、GPT-6 的具体作用、事件日期及依据、入口、许可状态和限制。没有代码填 `null`；没有确切日期不要猜。为英文 Gallery 同时补齐 `data/i18n.json` 中同 ID 的 title 和 summary。

指标必须说明分母和协议；“成功片段”“全部 trials”“全部 models”和“辅助 reset”不能混计。不能用 46/100 的进度分数替换 7/100 的完全成功率。没有原帖时保留镜像或二手等级。

来源 ID、可访问方式和逐项说明见 [SOURCES.md](docs/SOURCES.md)，日期事件含义见 [PUBLICATION_DATES.md](docs/PUBLICATION_DATES.md)。贡献者提交是新的证据，不会自动改变既有核验状态。

```bash
python scripts/validate.py
python scripts/build.py
python -m unittest discover -s tests -v
```

如有**可直接链接、可核验的公开 Demo 图片**，写入 `data/media.json`：必须关联该项目已有的 `source_id`、原始上下文 URL、中英文 alt/caption，且不复制或上传第三方视频/截图。没有此类媒体时不要用生成图、装饰图或搜索缩略图替代；由构建器保留原始入口并生成明确缺项说明。

不要直接编辑自动生成的 CATALOG.md、SOURCES.md、HUGGING_FACE.md、MEDIA.md、projects.csv 或 site/index.html；编辑 JSON 和 site/template.html 后构建。

## 不接受

不接收私有仓库/内部材料、未经授权的付费内容镜像、密钥、认证文件、模型权重转存、非授权视频或字体。无需复制上游代码来提交条目。只链接合法公开来源，并尊重删除、更正和许可要求。

新增机器人运行命令不得绕过急停、动作校验、访问权限或现场监督；本目录的默认 CI 必须保持离线，不自动执行机器人、下载大模型或调用计费服务。
