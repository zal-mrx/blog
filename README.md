# 昨日晴空的小窝

一个用 **Hexo + Butterfly** 搭的个人博客，配色是深青色「雨后海面」，首屏带云海背景、打字机副标题和波浪分隔。

**线上地址：<https://guileless-narwhal-616d5f.netlify.app/>**
**代码仓库：<https://github.com/zal-mrx/blog>**

改完内容提交推送，Netlify 会自动重新部署，几十秒后线上就更新了。

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
title: 昨日晴空的小窝          # 站点名，会显示在导航栏和首屏
description: '...'        # 一句话简介
author: 昨日晴空
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

`source/img/` 里的图，直接同名覆盖即可，不用改代码：

| 文件 | 用在哪 |
|---|---|
| `banner.jpg` | 电脑端首屏背景（1920×1080） |
| `banner-mobile.jpg` | 手机端首屏背景（1080×1620，竖图） |
| `avatar.png` | 头像 + 导航栏 logo + favicon（正方形，建议 240×240 以上） |
| `cover-1.jpg` / `cover-2.jpg` | 文章封面（800×500 左右） |
| `banner-cloud.jpg` | 之前那张云海背景，留着备用的，没在用 |

现在的首屏是用插画 `hero-source.jpg`（放在项目根目录）合成的：`make_hero.py` 会把人像从白底抠出来，贴到深色渐变上，同时生成电脑版和手机版。
想重新调整人物位置/大小，改 `make_hero.py` 末尾两个 `compose(...)` 的参数（`fg_h` 大小、`x0/y0` 位置），然后：

```bash
python make_hero.py      # 需要 Pillow 和 numpy
```

生成的预览在 `../shots/` 目录，满意了再复制成 `source/img/banner.jpg` 和 `banner-mobile.jpg`。

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

## 四、线上部署（已完成）

站点已经跑在 **Netlify** 上，从 GitHub 仓库自动构建：

- 仓库：`zal-mrx/blog`
- 构建命令：`npm run build`，发布目录：`public`
- 每次 `git push` 后，Netlify 自动重新部署，约 1 分钟生效

### 怎么更新内容

在本机 `myblog` 目录执行：

```bash
git add -A
git commit -m "写点说明"
git push
```

推完等一分钟，线上就是新的了。

> **为什么不用 Vercel？** `*.vercel.app` 在大陆被 DNS 污染（解析到 199.193.116.105 黑洞），打不开；`*.netlify.app` 实测 660ms 可通。
> 如果以后 Netlify 也不行了，备选：Cloudflare Pages（`pages.dev` 实测也可通，构建命令同样填 `npm run build`、目录 `public`）。

### 想用自己的域名

- 域名在阿里云 / 腾讯云 / Namecheap 买，一年几十块
- Netlify 后台 **Domain management → Add a domain**，按提示去域名商加一条 CNAME 记录
- 换域名后记得同步改 `_config.yml` 里的 `url:`
- **注意**：服务器或 CDN 放在中国大陆境内，域名必须做 ICP 备案；Netlify 这类境外托管则不需要备案

---

## 五、常见问题

**Q：改了配置没生效？**
A：`_config.yml` 和 `_config.butterfly.yml` 的改动要重启预览（关掉窗口重开）。

**Q：评论 / 留言板怎么用？**
A：已经接好了 **Giscus**（评论存在 `zal-mrx/blog` 仓库的 Discussions 里，免费、无广告、永久保存）。访客用 GitHub 账号登录即可留言；你可以在 GitHub 仓库的 **Discussions** 标签里看到并回复所有评论。
相关配置在 `_config.butterfly.yml` 的 `comments:` 和 `giscus:` 两段，`repo_id` / `category_id` 都是绑定的，别乱改。

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
