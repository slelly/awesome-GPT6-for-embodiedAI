# 发布到 GitHub

这是可发布的源文件包，**当前没有代为创建或推送远程仓库**。先检查仓库内容、LICENSE、README 中的快照范围和引用，再决定公开。

## 命令行发布

在解压出的 `awesome-gpt6-embodied` 目录运行。以下命令会创建公开仓库，执行前确认当前 GitHub 账户和目标名称正确；本次并未执行这些写操作。

```bash
python scripts/validate.py
python scripts/build.py
python -m unittest discover -s tests -v

git init -b main
git add .
git commit -m "Add evidence-aware GPT6 embodied AI catalogue"

# 使用你自己的授权账户；不在聊天或仓库中填写 token
# 已授权时可跳过登录
gh auth login
gh repo create awesome-gpt6-embodied --public --source=. --push
```

如果同名仓库已经存在，不执行 `gh repo create`；改为检查对应 remote 后按你现有的发布流程推送。不要覆盖别人的分支或历史。

建议 description：`Evidence-aware GPT-6 Astra robotics, policy control, real2sim and evaluation resources.`

建议 topics：`awesome-list`, `embodied-ai`, `robotics`, `gpt-6`, `astra`, `vision-language-action`, `real2sim`, `robot-learning`。这些只是仓库元数据建议，不是认证标签。

## GitHub Pages

`site/index.html` 是自包含静态目录，无后端和密钥。可以只把 `site/` 作为静态站点根目录。随包提供 `.github/workflows/pages.yml`，**仅可手动触发**，不会在普通 push 时自动发布。

在 GitHub 仓库 Settings → Pages 选择 GitHub Actions，然后在 Actions 手动运行 `Publish catalogue page`。workflow 会校验、构建、上传 `site/` 并部署。组织权限或 Pages 设置可能影响操作；请按当时 GitHub 界面核对。若不需要网站，可删除该 workflow。

只部署静态网站，不公开模型认证、机器人服务、标注接口或运行日志。网页“导出当前 JSON”在用户浏览器本地生成文件，不把查询上传到服务端。

## 更新目录

1. 修改 `data/projects.json`、`data/sources.json` 或 `data/artifacts.json`。
2. 按规则注明来源、日期、角色、许可与限制；必要时更新快照元信息与 README 数量。
3. 运行离线 validate / build / tests，检查生成文档与网页，再提交。

变更记录放在 CHANGELOG.md。不要为了让 CI 通过而把未知值改成猜测；使用 null、未确认标记和限制说明。
