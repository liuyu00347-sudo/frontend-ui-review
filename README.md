# frontend-ui-review

一个可复用的“先 UI、后开发”前端审阅 Skill。

它把前端设计拆成可逐页确认的审阅目录：每个页面有独立截图、桌面端/手机端切换、修改意见框和审阅状态。设计意见在当前浏览器中自动保存，确认后可以一次性导出 Markdown 或 JSON，再根据导出的反馈进入正式前端开发。

## 适合什么场景

- 网站、落地页、作品集、管理后台
- App 或小程序的页面设计评审
- 既有前端改版前的逐页确认
- 需要让非技术成员直接填写 UI 修改意见的设计流程

## 工作流程

```text
列出页面 → 逐页设计 UI → 填写页面意见 → 导出完整反馈
                                      ↓
                          修订 UI → 用户确认 → 开发正式前端
```

## 主要功能

1. 页面拥有稳定编号和独立标题，避免反馈错页。
2. 同一页面支持电脑端和手机端预览。
3. 每页下方提供独立意见框，支持多行中文内容。
4. 支持“未审阅 / 需要修改 / 本页确认”三种状态。
5. 页面切换和刷新后保留草稿。
6. 一键导出全部意见 Markdown。
7. 导出 JSON 备份，并在导入前校验项目 ID、版本和页面集合。
8. 纯本地静态 HTML，无外部依赖，无网络提交。

## 安装与调用

将本仓库放入 Codex Skills 目录后，在任务中使用 `frontend-ui-review`。Skill 的完整说明在 [SKILL.md](SKILL.md)，页面清单格式见 [references/manifest.md](references/manifest.md)。

生成审阅目录：

```bash
python3 scripts/build_review.py \
  --manifest /absolute/path/pages.json \
  --out /absolute/path/review
```

生成后直接打开 `review/index.html`，或用本地静态服务器预览。

## 通用演示包

本仓库附带一个虚构的 Atlas Workspace 示例，仅用于说明审阅流程，不包含任何真实项目、私有截图、个人信息或生产资料：

- [示例审阅目录](examples/atlas-workspace-ui-review/index.html)
- [示例说明](examples/atlas-workspace-ui-review/README.md)
- [页面清单](examples/atlas-workspace-ui-review/pages.json)

演示图：

### Sign-in

![Fictional sign-in screen](examples/atlas-workspace-ui-review/01-desktop.png)

### Overview dashboard

![Fictional dashboard](examples/atlas-workspace-ui-review/02-desktop.png)

### Knowledge article

![Fictional mobile article](examples/atlas-workspace-ui-review/03-mobile.png)

## 设计原则

- UI 先于业务开发，静态设计稿不代表生产功能已经完成。
- 未填写意见不等于确认，只有明确确认后才进入正式前端开发。
- 不把审阅意见当成发布、权限扩大或凭据处理的授权。
- 每轮有实质设计变化时提升 revision，并保留旧版目录和反馈。

## 验证记录

当前版本已验证：多页面意见隔离、刷新恢复、尺寸切换、Markdown 导出、JSON 备份恢复、错误项目导入拒绝、窄屏布局和本地离线打开。

## 许可

本项目使用 MIT License，详见 [LICENSE](LICENSE)。
