---
title: 折腾了一圈 linter/formatter，我又回到了 eslint
date: 2025-05-19 16:52
excerpt: eslint, biome, oxlint 的比较
category: 前端
---
# 背景
最近想折腾一下 linter/formatter 了，主要是 eslint 体验很一般：
- v9 带来的 breaking changes 太大
  - flat config 的生态太差，很多插件的文档还是只提供旧的配置，没法直接复制，得自己手动翻译成 flat config 版本
  - 旧的配置迁移到 flat config 官方的迁移工具不好用，功能是等价了，但是不是最优的代码
  - 还放弃了对格式化的支持（开发者不建议用，但是可以强行用），现在直接用 eslint 进行 ts 的格式化体验不好
- 在大型仓库中，ESLint 的运行速度也较慢，影响开发效率

# 其他新选择
## oxlint
这个是最新前端工具链 oxc 的一部分，用 rust 编写并且有一些别的优化，比 eslint 快几十倍

浅尝了一下，主要发现这几个比较难受的点：

### 只支持 json 配置文件
并且出于[一些考虑](https://github.com/oxc-project/oxc/pull/2214)，未来也只支持 json 配置文件

虽然 json 和 js 的生态非常相关，而且 oxlint 也支持 jsonc，在 js 这里我还是更喜欢用这个语言给自己写注释，而不是引入什么 DSL（点名批评 Prisma，虽然 json 已经流行到不算什么 DSL 了）

### 不支持 html lint
这个是最难绷的，oxlint 也是 voidzero 的成员，居然不先把自家框架 vue 支持了

而且这个支持看起来遥遥无期，[不在官方计划内](https://github.com/oxc-project/oxc/issues/8171)，不过第三方社区可能会提交支持

### 不支持 formatter
我个人是不太愿意再用 prettier 的，formatting 方案是 oxlint + prettier，那我为啥不用 eslint + prettier 呢

### 生态不足
这个应该无需多言了，看眼文档中的[插件列表](https://oxc.rs/docs/guide/usage/linter/plugins.html)就清楚了

而且从中文技术社区（知乎、v2ex、linux.do、掘金等）来看，搜索 oxlint 得到的内容寥寥无几

很难不让人怀疑这是个玩具项目，有无数的坑等着使用者踩，我先缩了，等别人踩踩再说

而且从 github 来看，oxc 的人手非常不足，oxlint 很依赖核心开发者并且特性推进缓慢

## biome
也是一个 linter，同样性能比 eslint 好很多

### 只支持 json 配置文件
这一点和 oxlint 一样

### 勉强支持 html
虽然目前（2025-05-19） biome 还不支持 html lint，但是在 2.0 beta 版里支持了，这个是一个很大的利好

### 支持 formatter
比 oxlint 好很多，至少不用多一个依赖了

# 总结
对于我的使用场景来说，自己的小项目没有性能瓶颈，完全不需要从 eslint 切换到别的依赖

对于公司的项目来说，没有 monorepo 的基础（内网连 pnpm 都没有），也不需要考虑性能问题

而且只能使用某些版本的二进制文件（vscode 和插件），只能使用低版本 eslint，我还是不切换了吧

等 biome v2 稳定后，我可能会在一些小项目上试用 biome，当前还完全没有必要