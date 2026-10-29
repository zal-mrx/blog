# 云曦的小窝

一个用 **Hexo + Butterfly** 搭的个人博客，配色是深青色「雨后海面」，首屏带云海背景、打字机副标题和波浪分隔。

本地已经能跑了，下一步是换成你自己的内容，然后发布到网上。

---

## 一、先看看效果

双击 **`打开博客.cmd`**，会自动开浏览器访问 <http://127.0.0.1:4000>。

关掉预览：在那个黑色命令行窗口按 `Ctrl + C`，或直接关窗口。

> 说明：这台机器上原本没有 Node.js，所以我在 `..\tools\` 里放了一份绿色版 Node + npm。
> 上面那个 .cmd 会自动把它加进 PATH，你不用管。以后想全局用 `hexo` 命令，装一个官方 Node.js LTS 就行。

---

## 二、目录里都是什么

```
myblog/
├── _config.yml              # 站点总配置：标题、作者、网址、分页
├── _config.butterfly.yml    # 主题配置：导航、首屏、侧边栏、颜色
├── package.json             # 依赖清单
├── 打开博客.cmd             # 一键本地预览
├── source/
│   ├── _posts/              # 文章都放这里（Markdown）
│   ├── about/index.md       # 关于我
│   ├── categories/          # 分类页
│   ├── tags/                # 标签页
│   ├── css/custom.css       # 自定义样式（标题、波浪、卡片圆角）
│   └── img/                 # 背景图、头像、封面
├── scaffolds/               # 新建文章的模板
└── public/                  # 生成的静态网站（不用手动改）
```

---

## 三、怎么换成一个「你的」博客

### 1. 改基本信息

打开 `_config.yml`，改这几行：

```yaml
title: 云曦的小窝          # 站点名，会显示在导航栏和首屏
description: '...'        # 一句话简介
author: 云曦
language: zh-CN
```

打开 `_config.butterfly.yml`，改：

```yaml
menu:                     # 导航栏，格式：名称: 链接 || 图标
  主页: / || fas fa-home
  博文: /archives/ || fas fa-archive
  ...
social:                   # 你的 GitHub / 邮箱
  fab fa-github: https://github.com/你的用户名 || Github || '#24292e'
```

### 2. 换图片

`source/img/` 里放这三张就够：

| 文件 | 用在哪 |
|---|---|
| `banner.jpg` | 首屏背景（1920×1080 最好） |
| `avatar.png` | 头像 + 导航栏 logo + favicon（正方形，建议 240×240 以上） |
| `cover-1.jpg` / `cover-2.jpg` | 文章封面（800×500 左右） |

直接同名覆盖即可，不用改代码。想换成自己拍的照片，把图丢进去、文件名对上就行。

### 3. 写新文章

```bash
# 在 myblog 目录下
..\tools\node.exe node_modules\hexo\bin\hexo new "文章标题"
```

或者在 `source/_posts/` 里新建一个 `.md` 文件，头部这样写：

```markdown
---
title: 标题
date: 2026-10-30 20:00:00
categories:
  - 随笔
tags:
  - 日常
cover: /img/cover-1.jpg
description: 首页卡片上显示的一句话简介
---

正文用 Markdown 写。
```

保存后刷新浏览器就能看到（本地预览会自动重建）。

---

## 四、发布到网上（三种选一个）

> 前提：`_config.yml` 里的 `url:` 改成你的真实地址，否则文章里的分享链接会是 example.com。

### 方案 A：Vercel（推荐，免费、免备案、自带 HTTPS）

1. 注册 <https://vercel.com>（用 GitHub 账号登录）
2. 把 `myblog` 整个文件夹传到一个 GitHub 仓库
3. Vercel → **Add New → Project** → 选这个仓库
4. 构建设置填：
   - Framework Preset: `Hexo`
   - Build Command: `npm run build`
   - Output Directory: `public`
5. 点 Deploy，几十秒后拿到 `xxx.vercel.app` 的网址

### 方案 B：Cloudflare Pages（同样免费免备案，国内访问略好）

Build command 填 `npm run build`，Build output directory 填 `public`。

### 方案 C：GitHub Pages

装 `hexo-deployer-git`，在 `_config.yml` 底部配置：

```yaml
deploy:
  type: git
  repo: https://github.com/你的用户名/你的用户名.github.io.git
  branch: main
```

然后 `hexo clean && hexo generate && hexo deploy`。

### 想用自己的域名

- 域名在阿里云 / 腾讯云 / Namecheap 买，一年几十块
- Vercel/Cloudflare 后台添加域名，按提示去域名商加一条 CNAME 记录
- **注意**：服务器或 CDN 放在中国大陆境内，域名必须做 ICP 备案；用 Vercel / Cloudflare 这类境外托管则不需要备案

---

## 五、常见问题

**Q：改了配置没生效？**
A：`_config.yml` 和 `_config.butterfly.yml` 的改动要重启预览（关掉窗口重开）。

**Q：想加评论 / 留言板？**
A：Butterfly 支持 Waline、Twikoo、Giscus。最省事的是 Giscus（直接用 GitHub Discussions，免费无后端），在 `_config.butterfly.yml` 的 `comments:` 里配置即可。

**Q：想加「相册」页？**
A：需要 `hexo-butterfly-...` 系列的相册插件，或自己写一个页面嵌图床。导航里先不加，免得点进去是空的。

**Q：字体/图标显示不出来？**
A：主题的第三方资源已经全部本地化（`CDN.third_party_provider: local`），不依赖 jsdelivr，国内访问也正常。

**Q：备份怎么办？**
A：整个 `myblog` 目录（除了 `node_modules` 和 `public`）就是一个完整的博客源码，推到 GitHub 就是备份，换电脑拉下来 `npm install` 就能继续写。

---

## 六、这个站的技术细节

- **框架**：Hexo 8.1.2
- **主题**：Butterfly 5.7.0
- **插件**：本地搜索（hexo-generator-searchdb）、首页/归档/分类/标签生成器
- **首屏波浪**：`source/css/custom.css` 里用 `mask-image` 实现，跟着明暗模式自动变色
- **背景图**：`make_banner.py` 用噪声算法生成，不是盗图，可自由替换
