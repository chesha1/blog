---
title: 使用 Durable Objects 固定 Cloudflare Workers 的执行位置
date: 2025-09-29 21:01
category: 云服务
excerpt: 使用 Durable Objects 的 locationHint 将 Cloudflare Workers 固定在指定区域执行
---
# 背景
很多时候有的服务对某些区域有限制，比如英国禁止成人网站的访问（这是本文的初衷），而 Cloudflare Workers 的执行位置是随机的，就会恰好撞上这种限制

而 [Cloudflare Workers 又倾向于将一个请求调度到一个已经启动好的热服务器上，而不是冷启动一个新的](https://blog.cloudflare.com/eliminating-cold-starts-2-shard-and-conquer/)，这就会导致多重试几次躲开这个区域限制不可行

# 为什么是 Durable Objects
Durable Objects 是 Cloudflare 的有状态计算服务，提供强一致性的单一执行上下文。每个对象实例在全球逻辑上只有一个，用于协调状态和处理并发。

正因为其“全局唯一实例”的特性，Durable Object 在首次创建时会在某个区域“落锤”，之后会保持该放置位置。因此，只要把需要固定区域执行的逻辑放进 Durable Object 的方法里，并在创建时给出区域提示，就能达到“固定执行位置”的效果。

# 做法
核心就一件事：在第一次创建 [Durable Object Stub](https://developers.cloudflare.com/durable-objects/api/stub/) 时，指定 `locationHint`。这个参数用于提示 Cloudflare 在哪个大区创建该对象。

`locationHint` 有一些固定的取值，比如 `apac`、`weur`、`wnam`，具体可以参考[文档](https://developers.cloudflare.com/durable-objects/reference/data-location/#supported-locations-1)

让我们来看一个完整的例子

```typescript
// src/index.ts
import { DurableObject } from "cloudflare:workers";

const TRACE_ENDPOINT = "https://www.cloudflare.com/cdn-cgi/trace";

export class MyDurableObject extends DurableObject<Env> {
	constructor(ctx: DurableObjectState, env: Env) {
		super(ctx, env);
	}

	async sayHello(name: string): Promise<string> {
		return `Hello, ${name}!`;
	}

	async lookupExecutionLocation(): Promise<string> {
		try {
			const response = await fetch(TRACE_ENDPOINT, {
				cf: {
					cacheTtl: 300,
					cacheEverything: true,
				},
			});

			if (!response.ok) {
				return "unknown-location";
			}

			const traceText = await response.text();
			const traceData = traceText
				.trim()
				.split("\n")
				.map(line => line.split("="))
				.reduce<Record<string, string>>((acc, [key, value]) => {
					if (key && value) {
						acc[key] = value;
					}
					return acc;
				}, {});

			const parts = [
				traceData.colo && `colo=${traceData.colo}`,
				traceData.loc && `loc=${traceData.loc}`,
			].filter(Boolean);

			return parts.length > 0 ? parts.join(", ") : "unknown-location";
		} catch (error) {
			console.warn("Failed to resolve execution location", error);
			return "unknown-location";
		}
	}
}

export default {
	async scheduled(event, env, ctx): Promise<void> {
		const stub = env.MY_DURABLE_OBJECT.getByName("foo-apac", { locationHint: "apac" });
		const [greeting, location] = await Promise.all([
			stub.sayHello("world"),
			stub.lookupExecutionLocation(),
		]);

		console.log(`[cron ${event.cron}] ${greeting} @ ${location}`);
	},
} satisfies ExportedHandler<Env>;
```
```javascript
// wrangler.jsonc
{
	"$schema": "node_modules/wrangler/config-schema.json",
	"name": "durable-object-starter",
	"main": "src/index.ts",
	"compatibility_date": "2025-09-27",
	"migrations": [
		{
			"new_sqlite_classes": [
				"MyDurableObject"
			],
			"tag": "v1"
		}
	],
	"durable_objects": {
		"bindings": [
			{
				"class_name": "MyDurableObject",
				"name": "MY_DURABLE_OBJECT"
			}
		]
	},
	"triggers": {
		"crons": [
			"54 12 * * *"
		]
	},
	"observability": {
		"enabled": true
	}
}
```
`lookupExecutionLocation()` 看起来可能有点长，但是不用管，只是为了打印执行的位置，你可以把它换成任意需要要固定位置执行的逻辑


还有一个注意点，如果之前用某个 name 调用 getByName 创建过这个 Durable Object Stub，再用同样的 name 和不同的 `locationHint` 创建，是不会生效的，需要换个名字

还有这类似于一个建议，我也遇到过换了 name 和 locationHint 还是不行的情况，不过再部署一次下次就好了，可能这也是一个建议，而不是强制地固定区域

# 效果
关于上面的示例代码，如果不指定 `locationHint`，多次执行的日志是这样 `[cron 0 9 * * *] Hello, world! @ colo=SCL, loc=CL`

换成 `locationHint: "apac"` 后，位置立即变了： `[cron 37 12 * * *] Hello, world! @ colo=SIN, loc=SG`

再换个区域试试 `locationHint: "weur"`，日志是 `[cron 54 12 * * *] Hello, world! @ colo=CDG, loc=FR`

