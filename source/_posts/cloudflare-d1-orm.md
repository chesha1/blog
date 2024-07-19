---
title: Cloudflare D1 的 ORM 选择：Prisma 还是 Drizzle
date: 2024-07-16 00:20
excerpt: Cloudflare D1 ORM，以及 Prisma 和 Drizzle 的比较
index_img: /img/cloudflare-d1-orm.webp
category: 前端
tags: 
  - Cloudflare D1
  - Prisma
  - Drizzle
---
# 前言
Cloudflare 提供了非常廉价的数据库服务 D1，在免费额度下，用户可以获得 5GB 的存储空间，每天支持 500 万行的读取和 10 万行的写入

因为同时使用了 Cloudflare 提供的大量其他免费服务，就想要一起使用 D1 作为服务的后端存储

虽然 D1 也提供了接口，可以执行 SQL 语句进行增删改查，但使用 ORM 框架更为方便高效。因此，这里选择了两个较为流行的 ORM 框架，Prisma 和 Drizzle，分别简单介绍它们在 Cloudflare 上的使用，并且进行对比


# Cloudflare D1 的小坑
尽管 Cloudflare D1 提供了大量免费额度，但在实际使用中，瓶颈并不在这里，而是在另一个方面

Cloudflare D1 的调用，并不像别的 Serverless 数据库服务，会给出一个连接串，Cloudflare D1 的所有调用都必须通过 Cloudflare Workers 在内网进行

而对于 Workers，在免费计划下，CPU 时间的最大值为 10ms

所以哪怕你只是稍微轻度地使用一下 Cloudflare D1，一共就只有几万行数据，每天就查几次，也大概会碰到这个瓶颈

如果你基于 Cloudflare 构建自己的有状态服务（需要数据库），很难不订阅月付 $5 的 Workers Paid，订阅后，每次 Workers 调用的最大时长被放宽到 30s

那么其他的 Serverless 平台呢？比如 Vercel

对于真正的小用量用户来说，Vercel 的数据库表现更好，至少在轻量使用情况下没有问题 

如果用量稍微上来一点，比如一共有几十万行，每天会读几百万行，那 Vercel 的免费计划就撑不住了，**但 Vercel 的最低付费计划需要每月 $25，远远超过 Cloudflare 的每月 $5**

因此，对于一个简单的服务来说，**Cloudflare Workers Paid 的性价比远高于 Vercel Pro Plan**，且价格更便宜，每月 $5 是一个非常有性价比的价格。

# Prisma
## 网络问题
Cloudflare 官方的这篇[文档](https://developers.cloudflare.com/d1/tutorials/d1-and-prisma-orm)很好，已经基本覆盖了所有内容，能够上手了，下面补充一些文档里没有提到的细节

大部分身处中国大陆的用户可能会遇到一些网络问题，这些问题比普通的依赖下载更为复杂

根据 [Prisma 的架构](https://www.prisma.io/docs/orm/more/under-the-hood/engines)，会有一个引擎来翻译被调用的高级 API

![](/img/cloudflare-d1-orm-1.png)

而这个引擎是一个二进制文件，下载起来就比代码构成的其他依赖就更加麻烦

如果遇到了其他网络问题，设置了代理等方法还不行，同时在使用 `pnpm install` 和 `pnpm dlx`，可以换回 `npm install` 和 `npx` 试试

## 基本使用
首先，数据库连接和表的定义都会放在 `prisma/schema.prisma` 下面

然后根据需要，进行数据库迁移，比如，你在本地声明式地添加了一张新表（`schema.prisma` 中的一个新 `model`），就需要对远程的数据库应用这一次迁移

对于 Cloudflare D1 来说，数据库迁移没有那么容易，可能是因为 Prisma 才支持 D1 不久，所以步骤比较繁琐，详情见[文档](https://developers.cloudflare.com/d1/tutorials/d1-and-prisma-orm#4-create-a-table-in-the-database)

然后用 `npx prisma generate` 生成 Prisma Client，生成的 Prisma Client 包含了类型定义，在写 Typescript 代码的时候就可以用到这些定义

在具体的使用中，对于 SQL 中的增删改查，Prisma 也有相应的函数，只是会稍微有一点不一样，可以参考[文档](https://www.prisma.io/docs/orm/prisma-client/queries/crud)

# Drizzle
和 Prisma 不同，使用 Drizzle 的负担小很多，没有二进制文件的依赖，Drizzle 仅仅是在原生 SQL 上添加了一层薄薄的抽象

首先需要一个 `db/schema.ts` 文件来定义表，比如：
```typescript
// db/schema.ts
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';

export const countries = sqliteTable('countries', {
    id: integer('id').primaryKey(),
    name: text('name'),
}
);
```
{% fold info @接下来，可以用 Drizzle 的数据库迁移功能，也可以自己写 sql 文件管理数据库结构，展开具体步骤 %}
然后在项目根目录中新建文件 `drizzle.config.ts`，配置数据库迁移的规则：

{% note success %}
注意，这里所说的数据库迁移，不是把数据从一个数据库搬到另一个数据库

在 ORM 的语境下，数据库迁移是指在同一个数据库中，改变表的结构，可以参考一下 [Prisma 的文档](https://www.prisma.io/docs/orm/prisma-migrate/getting-started)理解一下这个概念
{% endnote %}
```typescript
// drizzle.config.ts
import type { Config } from "drizzle-kit";

export default {
    schema: "./db/schema.ts",
    out: "./db/migrations",
    dialect: "sqlite",
    dbCredentials: {
        wranglerConfigPath: "wrangler.toml",
        dbName: "<your-db-name>",
    },
} satisfies Config;
```

然后用 `npx drizzle-kit generate` 生成迁移文件，注意产生的迁移文件需要跟着 Git 走，不然下次迁移就不好用了

在 `wrangler.toml` 中添加 `migrations_dir = "db/migrations"`

然后用 `npx wrangler d1 migrations apply <your-db-name> --remote` 应用迁移文件

{% endfold %}

然后直接在代码里使用这些定义，比如：
```typescript
import { drizzle } from 'drizzle-orm/d1';
import { countries } from './schema';

export interface Env {
	db: D1Database;
}

export default {
	async fetch(request: Request, env: Env) {
		const db = drizzle(env.db);
		const result = await db.select().from(countries).where(eq(countries.id, 5));
		return Response.json(result);
	},
};
```
除了像 Prisma 一样用一些高级的查询 API，这里可以像使用原生 SQL 语句一样使用 Drizzle，无疑从使用上来说友好很多，毕竟不需要学太多新东西

Prisma 也可以用一些[接近原生 SQL 的 API](https://www.prisma.io/docs/orm/prisma-client/queries/raw-database-access/raw-queries)，但是就需要直接自己写 SQL 语句的字符串了，这种抽象程度又有点过于低了，而且可能导致安全问题

# 选择 Drizzle 的原因
从功能上来说，Prisma 无疑比 Drizzle 丰富：支持更多的数据库类型，数据库迁移功能更好，查询时提供更多附加功能

但是这也带来了很多额外的负担：依赖二进制文件，需要 `.prisma` 这种新格式然后生成类型，整个框架很重

实际上，Prisma 官方就有[文档](https://www.prisma.io/docs/orm/more/comparisons/prisma-and-drizzle)和其他 ORM 框架对比，其中提到 Prisma 解决了很多许多传统 ORM 的问题：模型实例臃肿、业务与存储逻辑混合、缺乏类型安全性，由延迟加载等引起的不可预测的查询

**但是对于一个个人开发者，以上问题都不存在，为了简单起见，我选择使用 Drizzle，或许对于一个生产环境中的成熟商业产品，用 Prisma 更好**

有一些开发者也提到了 Prisma 存在的[各种问题](https://www.reddit.com/r/node/comments/14lyyia/prisma_vs_drizzle_orm_for_production/)

**关于性能，至少 Drizzle 不逊色于 Prisma**

在 Drizzle 的[官网](https://orm.drizzle.team/)上，有性能对比，Drizzle 明显优于 Prisma

在 Prisma 官方提供的[基准测试](https://db-latency.vercel.app/)上，Drizzle 和 Prisma 的性能相当

在一个[第三方测试](https://github.com/masfahru/typescript-orm-benchmark)上，Drizzle 略好于 Prisma

选择 Drizzle 的另一个原因是，Drizzle 的官网看起来很可爱

下图是 [Drizzle 的官网](https://orm.drizzle.team/)：
![](/img/cloudflare-d1-orm-2.png)

下图是 [Prisma 的官网](https://www.prisma.io/)：
![](/img/cloudflare-d1-orm-3.png)

下图是 [Prisma 的官网](https://typeorm.io/)：
![](/img/cloudflare-d1-orm-4.png)

Drizzle 的官网很生动，属于是一看就会喜欢的那种

# 其他痛点
虽然我们已经有了一个 Cloudflare D1，但这都只是在内网使用，Cloudflare D1 目前没有一个成熟的，可以部署在 Workers 上的框架，能把内网的数据库服务暴露给公网

一方面，这会失去内网进行服务绑定的安全性，其次，Workers 和 D1 内部的交互机制并不清楚，如果只是简单地做一个请求的转发，不知道会有什么问题

一个显而易见的瓶颈就是，Workers 有并发限制，无法承载过于高强度的访问，而如果数据库经历高强度读写，加入 Workers 这个中间层也会遇到并发问题

