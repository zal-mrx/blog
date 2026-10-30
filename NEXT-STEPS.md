# 项目进度 / 交接备忘

> 最后更新：2026-10-30 02:25
> 给未来的自己（或 AI）看的：从这里接着干就行。

## 一、现在是什么状态

| 项 | 值 |
|---|---|
| 线上地址 | **https://ysqxue.cn** （旧地址 guileless-narwhal-616d5f.netlify.app 仍可用） |
| 代码仓库 | https://github.com/zal-mrx/blog （SSH 推送） |
| 本地目录 | `C:\Users\LEGION\Documents\deepseek-harness\default-workspace\myblog` |
| 技术栈 | Hexo 8 + Butterfly 5.7 |
| 托管 | Netlify（从 GitHub 自动构建，`npm run build` → `public`） |
| 评论 | Giscus（存在 zal-mrx/blog 的 Discussions） |
| 站点名 | 昨日晴空的小窝 |
| 作者 | 昨日晴空（GitHub: zal-mrx，邮箱 2959537317@qq.com） |

## 二、已完成的功能

- 首屏：插画背景（桌面/手机两版）+ 11 条轮播文案 + 波浪分隔
- 导航：主页 / 博文 / 相册 / 分类 / 标签 / 留言板 / 关于我（液态玻璃样式 + 点击放大动效）
- 相册：`source/img/gallery/` 丢图自动生成，带灯箱
- 留言板：Giscus
- 侧边栏：作者卡片 → 公告 → 最新文章 → 归档 → 网站信息（分类/标签卡片已移除）
- 深色模式、本地搜索、手机适配

## 三、待办（明天接着做）

### 1. 域名 ysqxue.cn（✅ 已完成 2026-10-30）

- 阿里云信息模板「于烁奇」实名审核中（注册局审核，约 1 小时起）
- 状态查询：阿里云控制台 → 域名 → 信息模板
- 变「已实名」后：回域名搜索页买 `ysqxue.cn`（首年 ¥38）
- 买完后绑定 Netlify：
  1. Netlify → Domain management → Add a domain → 输入 `ysqxue.cn`
  2. 阿里云「解析设置」加记录：
     - `A` `@` → `75.2.60.5`
     - `CNAME` `www` → `guileless-narwhal-616d5f.netlify.app`
  3. 等 DNS 生效（10 分钟～2 小时），Netlify 自动签 HTTPS
  4. 改 `_config.yml` 的 `url:` 为 `https://ysqxue.cn`，推送
- **不需要备案**（托管在境外）

### 2. 其他可选项

- 首屏那 3 条旧文案（欢迎来到 YSQ 的小窝 / 在代码与文字之间来回散步 / 把生活里细小的光收进这里）要不要删
- 关于页邮箱是否做防爬虫处理（现在是明文 QQ 邮箱）
- 相册里的 4 张演示图换成真实照片
- 导航改成悬浮胶囊造型（可选）

## 四、注意事项

- **Netlify 免费额度**：300 信用点/月 ≈ 20 次部署，每次部署约 15 点。
  已用约 60%。**改动攒着一起推**，别为小改动单独部署。额度用完站点会暂停。
- **推送命令**需要用 SSH（`ssh.github.com:443`），因为 github.com:443 在这台机器上不通。
  SSH 密钥在 `../home/.ssh/id_ed25519`，Git 的 SSH 配置已写入仓库的 `.git/config`。
- 本地工具链在 `../tools/`（node.exe、npm、git），没有装到系统里。
- 本地预览：双击 `myblog/打开博客.cmd`，或
  `..\tools\node.exe node_modules\hexo\bin\hexo server -p 4000`

## 五、常用操作

```bash
# 写新文章
..\tools\node.exe node_modules\hexo\bin\hexo new "标题"

# 本地预览
..\tools\node.exe node_modules\hexo\bin\hexo server -p 4000

# 发布（改完内容后）
git add -A
git commit -m "说明"
git push
```
