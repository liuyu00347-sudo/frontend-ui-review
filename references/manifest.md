# 审阅清单与反馈格式

构建清单使用 UTF-8 JSON。图片路径相对于清单所在目录，必须在该目录内部；不接受远程 URL。页面 ID 与视图 ID 用英文字母、数字、点、短横线或下划线。projectId 跨轮稳定，revision 在设计改动后提升。

```json
{
  "projectId": "sample-product",
  "title": "产品界面审阅",
  "revision": "ui-v1",
  "description": "设计稿，使用示例数据；请逐页填写意见后统一导出。",
  "entries": [
    {
      "id": "01",
      "title": "首页",
      "kind": "页面",
      "note": "品牌首屏、功能入口和主要操作。",
      "views": [
        {"id": "desktop", "label": "电脑端 · 1440px", "image": "images/home-desktop.png"},
        {"id": "mobile", "label": "手机端 · 390px", "image": "images/home-mobile.png"}
      ]
    }
  ]
}
```

兼容简写：entry 中使用 `desktop`、`tablet`、`mobile` 图片字段即可，不必写 views。App 可只有一个 mobile 视图。关键弹窗可设 `kind: "弹窗"`，并使用独立 ID。

构建器输出 index.html、review-manifest.json 和按 `<页面ID>-<视图ID>.<后缀>` 命名的图片。它不会清空输出目录，也不会写浏览器意见。

## 浏览器草稿与导出

localStorage 键：`frontend-ui-review:v1:<projectId>:<revision>`。修改浏览器、协议、域名或端口会改变可见存储；跨环境请先导出 JSON，再导入同一版本。

JSON 备份 schema 为 `frontend-ui-review-feedback/v1`，字段：

- projectId、projectTitle、revision、exportedAt、updatedAt。
- globalNotes：整个项目的统一意见。
- pages：所有页面，含 id、title、kind、status、notes、updatedAt、views。
- status 为 unreviewed / changes / approved。
- views 含图片文件名和 SHA-256，供核对所审阅的图版。

Markdown 用于发送给助手阅读，逐页包含上述身份、状态与意见；JSON 用于草稿迁移和自动化回读。所有页面都导出，未填写标记“未填写”，不遗漏未审页。导出不清空草稿，不上传任何服务器。

导入拒绝其他 projectId、其他 revision、缺失/重复/未知页面、非法状态或超过 10MB 的文件；通过校验后仍需点击“确认导入”。同版本同清单图片如果已经实质变化，应先提升 revision，不以导入绕过版本对应关系。
