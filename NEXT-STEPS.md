# 项目进度 / 交接备忘

> 最后更新：2026-11-19 20:40
> 给未来的自己（或 AI）看的：从这里接着干就行。

## 一、现在是什么状态

| 项 | 值 |
|---|---|
| 线上地址 | **https://ysqxue.cn**（Vercel） |
| 主域名 | `ysqxue.cn` → A `216.198.79.1` |
| www | `www.ysqxue.cn` → CNAME `c5ddf33235e4640a.vercel-dns-017.com` → 308 跳到主域名 |
| 旧地址 | `guileless-narwhal-616d5f.netlify.app`（Netlify，2026-11-02 起停止部署，留作备份） |
| 代码仓库 | https://github.com/zal-mrx/blog （SSH over 443 推送） |
| 本地目录 | `C:\Users\LEGION\Documents\deepseek-harness\default-workspace\myblog` |
| 技术栈 | Hexo 8 + Butterfly 5.7 |
| 托管 | **Vercel**（GitHub 推送自动构建，`npm run build` → `public`） |
| 访问统计 | 不蒜子 busuanzi（页脚「本站访客数 / 本站总浏览量」+ 文章「浏览量」） |
| 评论 | Giscus（存在 zal-mrx/blog 的 Discussions） |
| 站点名 | 昨日晴空的World |
| 作者 | 昨日晴空（GitHub: zal-mrx） |

## 二、DNS（阿里云，TTL 600）

| 类型 | 主机记录 | 记录值 |
|---|---|---|
| A | `@` | `216.198.79.1` |
| CNAME | `www` | `c5ddf33235e4640a.vercel-dns-017.com` |

> 注意：Vercel 的 A 记录**不是**网上常见的 `76.76.21.21`，以 Vercel 后台 Domains 页面实际显示的为准。

## 三、已完成的功能

- 首屏：插画背景（桌面/手机两版）+ 11 条轮播文案 + 波浪分隔
- 导航：主页 / 博文 / 相册 / 留言板 / 说说 / 分享 / 关于我（液态玻璃样式 + 点击放大动效）
- 相册：3D 旋转照片墙（15 张），`source/img/gallery/` 丢图自动索引，带灯箱、下雪/音乐开关
- 说说 / 分享 / 关于我（名片式，含天气、日期、音乐、抖音位）
- 留言板：Giscus
- 侧边栏：作者卡片 → 公告 → 最新文章 → 归档 → 网站信息
- 深色模式、本地搜索、手机适配
- 访问统计：不蒜子（2026-11-19 开启）

## 四、当前待办（都可选）

- 首屏那 3 条旧文案（欢迎来到 YSQ 的小窝 / 在代码与文字之间来回散步 / 把生活里细小的光收进这里）要不要删
- 相册里的 4 张演示图换成真实照片
- 导航改成悬浮胶囊造型
- Netlify 旧站点要不要删（不删也能当备份）

## 五、注意事项

- **Vercel 免费额度**：Hobby 计划每天 100 次部署，构建每月 6000 分钟，个人博客完全够用。
- **Netlify 已停用**：免费版 300 信用点/月 ≈ 20 次部署，2026-11-02 用完后生产部署被暂停（站点仍能访问，只是发不了新版本）。11 月底额度会重置，但已不再使用它部署。
- **推送命令**用 SSH（`ssh.github.com:443`），因为这台机器上 `github.com:443` 不通。
  SSH 密钥在 `../home/.ssh/id_ed25519`，私钥权限已收紧为仅当前用户可读（权限过宽 ssh 会拒绝使用）。
- 本地工具链在 `../tools/`（node.exe、npm、git），没有装到系统里。
- 本地预览：双击 `myblog/打开博客.cmd`，或
  `..\tools\node.exe node_modules\hexo\bin\hexo server -p 4000`
- 不蒜子统计是页面加载计数，**刷新也会 +1**，UV 按浏览器本地标记算，数字偏大属正常，看趋势即可。
  开关在 `_config.butterfly.yml` 的 `busuanzi:` 段，三个值改回 `false` 就关掉。

## 六、常用操作

```bash
# 写新文章
..\tools\node.exe node_modules\hexo\bin\hexo new "标题"

# 本地预览（改完配置要重启才生效）
..\tools\node.exe node_modules\hexo\bin\hexo server -p 4000

# 构建检查（可选，Vercel 会自己构建）
..\tools\node.exe node_modules\hexo\bin\hexo generate

# 发布（改完内容后）
git add -A
git commit -m "说明"
git push
```

推送后 Vercel 自动构建，**约 1 分钟**线上更新。

## 七、2026-11-19 迁移记录（Netlify → Vercel）

**原因**：Netlify 免费额度 11-02 耗尽，生产部署暂停，导致 11-02 的《今天好冷》和之后的改动一直没上线。Vercel 每天 100 次部署，更适合频繁更新。

**做了什么**：
1. Vercel 项目 `blog`（团队 `qixue`）本来就通过 GitHub 集成在自动构建，只是域名没指过去
2. Vercel 添加 `ysqxue.cn`（Production），按提示把阿里云 `@` 的 A 记录从 `75.2.60.5` 改为 `216.198.79.1`
3. 添加 `www.ysqxue.cn`，设为 308 跳到主域名，阿里云 `www` 的 CNAME 改为项目专属值
4. 同时开启不蒜子访问统计

**踩过的坑**：
- 同一个面板同时加 apex 和 www 会报 `Domain overlaps another row`，只填 apex 即可
- 不取消勾选 `Include apex and www variants`，www 跳 apex 会报 `A domain cannot redirect to itself`
- Vercel 页面上的复制按钮经常 `Failed to copy to clipboard`，宁可截图核对也别手打
- `*.vercel.app` 默认域名在国内被 DNS 污染（解析到 `103.228.130.27`），必须用自定义域名

完整建站过程见同目录 `..\网站搭建全记录.md`。
