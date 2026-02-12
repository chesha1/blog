# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hexo 8.1.1 静态博客，使用 hexo-theme-fluid 主题，pnpm 管理依赖。
站点语言 zh-CN，部署在 https://echoccc.online。

## Commands

```bash
pnpm dev        # 本地开发服务器 (hexo server)
pnpm build      # 生成静态文件到 public/ (hexo generate)
pnpm clean      # 清理缓存和生成文件 (hexo clean)
```

## Architecture

- `_config.yml` — Hexo 主配置（站点信息、URL、永久链接格式 `posts/:title/`）
- `_config.fluid.yml` — Fluid 主题配置（1100+ 行，控制外观、功能开关、CDN 等）
- `source/_posts/` — 已发布文章（Markdown）
- `source/_posts/hide/` — 隐藏/草稿文章（使用 `.hide` 后缀阻止渲染）
- `source/about/index.md` — 关于页面
- `source/img/` — 图片资源
- `scaffolds/` — 文章模板（post.md, page.md, draft.md）
- `mermaid/` — Mermaid 图表源文件

## Content Conventions

文章 front-matter 格式：
```yaml
---
title: 标题
date: YYYY-MM-DD HH:mm
excerpt: 摘要
index_img: /img/xxx.jpg    # 可选，首页缩略图
category: 分类名            # 可选
tags:                       # 可选
  - tag1
  - tag2
---
```

隐藏文章方式：将文件放入 `source/_posts/hide/` 并添加 `.hide` 后缀。

## Key Plugins

- `hexo-generator-feed` — RSS feed 生成
- `hexo-webp-cloud-proxy` — 图片通过 WebP Cloud CDN 代理加速（pre_url → proxy_url 映射）
- Fluid 主题内置 Mermaid 流程图支持（已启用）
