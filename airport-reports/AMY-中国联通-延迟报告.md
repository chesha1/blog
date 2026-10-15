# amy 机场延迟报告

**测试范围：全量节点。** 去重后订阅节点 56 个；本次选中 56 个，有有效记录 56 个，完成全部计划采样 56 个。
**订阅节点覆盖率：100.0%；计划样本覆盖率：100.0%。**节点有记录或采样完成不表示请求成功；成功、失败与无法判定分别统计。
全部去重订阅节点均已完成计划采样。

| 机场 | 订阅原始节点 | 去重节点 | 选中节点 | 有记录节点 | 完整采样节点 | 订阅节点覆盖率 | 有效样本/计划 | 样本覆盖率 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amy | 58 | 56 | 56 | 56 | 56 | 100.0% | 336/336 | 100.0% |

测试时间：2026-10-15T14:11:55.128212+00:00 至 2026-10-15T14:13:24.297147+00:00。状态：completed。
网络路径记录：interface-bound。
网络说明：中国联通流量（用户提供）；Windows 原生运行；物理 WLAN 接口 Up，ifIndex 18，存在默认路由；宿主 Mihomo TUN 开启；独立测试内核绑定 WLAN；未做全链路路径审计。

测试环境：python\_version=3.13.10；system=Windows；release=11；machine=AMD64；is\_wsl=False；mihomo\_version=1.19.31。

计划 336 个样本，有效记录 336 个，覆盖率 100.0%；缺测 0 个。成功 336、失败 0、无法判定 0。

原始记录 336 行；排除 0 行。排除原因见数据检查；原始 CSV 保持不变。

## 方法与分母

- 订阅节点覆盖率 = 本次选中节点中有有效记录的节点数 / 订阅去重节点总数。完整采样节点要求该节点的每个计划目标、类型和轮数均有有效唯一记录，failure 与 unknown 也属于已采样。缺少订阅计数时不能判断是否全量；缺少 schedule.json 时不确认完整采样节点数，未知数值以 — 表示。
- 仅完整的有效记录进入统计。有 schedule.json 时按计划中的序号、轮数、机场、节点、类型和目标核对，并用计划实际条目数作为分母；重复序号只保留首条有效记录。无 schedule.json 的旧数据只校验完整性及已提供的序号。
- 已观测成功率 = success / (success + failure + unknown)。unknown 单独列出；missing 不进入已观测分母。
- 已判定成功率 = success / (success + failure)，另存于 CSV/JSON；不把它当作完整样本成功率。
- 节点等权成功率：先计算每个有记录节点的已观测成功率，再对这些节点取算术平均。完全缺测的节点不参与平均，节点覆盖数与样本覆盖率同时列出。
- 延迟仅对成功请求的 elapsed_ms 计算 p50/p95；这是完整 HTTPS 请求耗时，不是 ICMP RTT。失败不补零。分位数按 (n−1)×p 线性插值。
- 不同探测目标单独展示。分位数描述成功样本，须连同失败、无法判定、缺测计数阅读，以免产生幸存者偏差。
- 地区按固定规则从订阅名称及别名归类，表示订阅声明的国家/地区，不是 GeoIP 或实际出口位置测量。未知或存在地区冲突的节点保留采样统计，不参与最快合格节点选择。
- 各地区、目标和测试类型单独统计。地区内先计算每节点成功请求的 p50，再对节点 p50 取中位数，让各节点等权；无有效成功数值的节点不补零，另列有数值节点/计划节点及失败分母。地区的请求合并 p50/p95 在采样明细中列出，仅供分布描述。
- 本次加权延迟 = 80.0% × F + 20.0% × M，单位 ms，越低越好。F 为该地区所选最快合格节点在当前目标上的多轮延迟中位数，M 为上述地区节点等权 p50 中位数。权重来源：原测量参数；两项原始数值同时保留供复算。
- 最快节点的资格：必须有可核验的 schedule.json，全部配置的延迟目标各至少 3 个计划样本，所有计划样本完整、成功且耗时有效，无失败、无法判定、缺测或多余样本。按各目标的节点 p50 算术平均选择最小者，并以匿名节点 ID 固定处理平局。同一地区同一机场的各目标始终使用同一个节点，不逐目标拼接不同节点的最好成绩。最快依据多轮中位数，不是最小单次请求。
- 最快资格的计划核验：通过；节点、全部目标及 1 至配置轮数的计划身份完整且唯一。
- 无合格节点时最快节点及加权延迟为空；仅当最快节点权重显式设为 0 时可单独使用 M。原有成功、失败、无法判定、缺测和覆盖率仍保留。
- 配置：延迟轮数 3，顺序种子 20261015，超时 5 秒；本次未进行下载测速。
- 执行参数：延迟并发 4；延迟按固定批次执行。Mihomo 出口绑定接口：WLAN；运行总时限 574 秒（来源：automatic）。

## 目标采样与成功计数

| 机场 | 类型 | 目标 | 样本/计划 | 覆盖率 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 节点等权成功率 | 有记录节点/节点 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amy | latency | https://cp.cloudflare.com/generate\_204 | 168/168 | 100.0% | 168 | 0 | 0 | 0 | 100.0% | 100.0% | 56/56 |
| amy | latency | https://www.gstatic.com/generate\_204 | 168/168 | 100.0% | 168 | 0 | 0 | 0 | 100.0% | 100.0% | 56/56 |

总体仅汇总采样与成功计数；延迟按各地区、各目标分别展示。

## 各地区延迟表现

F 为所选最快合格节点在当前目标的 p50，M 为地区各节点成功请求 p50 的中位数，W 为加权延迟。每个地区的各目标使用同一个已通过全部目标资格检查的节点；最快节点 p95 和成功样本/计划数同时列出。p95 只是本次小样本分布的描述。全失败或无合格节点的地区仍保留，无法计算的数值以 — 表示。

| 地区 | 目标 | 所选匿名节点 | 最快 F ms | 最快节点 p95 ms | 最快样本/计划 | 典型 M ms | 加权 W ms | 合格/候选节点 | 资格状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 香港 | https://cp.cloudflare.com/generate\_204 | amy-a09c6020552c-1634ec436acd | 183.79 | 449.24 | 3/3 | 218.48 | 190.73 | 21/21 | 已选择 |
| 香港 | https://www.gstatic.com/generate\_204 | amy-a09c6020552c-1634ec436acd | 186.35 | 441.25 | 3/3 | 227.60 | 194.60 | 21/21 | 已选择 |
| 日本 | https://cp.cloudflare.com/generate\_204 | amy-530735ac817f-b90a3ea726d7 | 233.33 | 457.00 | 3/3 | 297.53 | 246.17 | 8/8 | 已选择 |
| 日本 | https://www.gstatic.com/generate\_204 | amy-530735ac817f-b90a3ea726d7 | 205.36 | 452.66 | 3/3 | 308.82 | 226.05 | 8/8 | 已选择 |
| 新加坡 | https://cp.cloudflare.com/generate\_204 | amy-15ccc6a594b8-f63edcd31d79 | 277.99 | 502.83 | 3/3 | 281.89 | 278.77 | 4/4 | 已选择 |
| 新加坡 | https://www.gstatic.com/generate\_204 | amy-15ccc6a594b8-f63edcd31d79 | 265.62 | 472.22 | 3/3 | 273.22 | 267.14 | 4/4 | 已选择 |
| 台湾 | https://cp.cloudflare.com/generate\_204 | amy-182c1c20a6a0-9ac167ced453 | 235.08 | 459.62 | 3/3 | 276.12 | 243.29 | 10/10 | 已选择 |
| 台湾 | https://www.gstatic.com/generate\_204 | amy-182c1c20a6a0-9ac167ced453 | 259.23 | 417.90 | 3/3 | 254.60 | 258.30 | 10/10 | 已选择 |
| 美国 | https://cp.cloudflare.com/generate\_204 | amy-8fea2cd018c5-7ba05af9d3ca | 897.50 | 1125.97 | 3/3 | 938.29 | 905.66 | 13/13 | 已选择 |
| 美国 | https://www.gstatic.com/generate\_204 | amy-8fea2cd018c5-7ba05af9d3ca | 779.25 | 964.11 | 3/3 | 771.73 | 777.75 | 13/13 | 已选择 |

## 各地区采样明细

按地区、目标和测试类型保留全部计划分母。下表的 p50/p95 合并该地区该目标的成功请求，与上表先按节点取中位数的 M 口径不同。地区未知和地区冲突保留采样结果，不选择最快合格节点或计算加权延迟。

| 地区 | 目标 | 有记录节点/计划节点 | 样本/计划 | 覆盖率 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 有数值节点/计划节点 | 有效数值数 | 成功请求 p50 ms | 成功请求 p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 香港 | https://cp.cloudflare.com/generate\_204 | 21/21 | 63/63 | 100.0% | 63 | 0 | 0 | 0 | 100.0% | 21/21 | 63 | 221.19 | 548.46 |
| 香港 | https://www.gstatic.com/generate\_204 | 21/21 | 63/63 | 100.0% | 63 | 0 | 0 | 0 | 100.0% | 21/21 | 63 | 229.66 | 533.53 |
| 日本 | https://cp.cloudflare.com/generate\_204 | 8/8 | 24/24 | 100.0% | 24 | 0 | 0 | 0 | 100.0% | 8/8 | 24 | 297.53 | 510.83 |
| 日本 | https://www.gstatic.com/generate\_204 | 8/8 | 24/24 | 100.0% | 24 | 0 | 0 | 0 | 100.0% | 8/8 | 24 | 308.82 | 519.93 |
| 新加坡 | https://cp.cloudflare.com/generate\_204 | 4/4 | 12/12 | 100.0% | 12 | 0 | 0 | 0 | 100.0% | 4/4 | 12 | 282.29 | 534.94 |
| 新加坡 | https://www.gstatic.com/generate\_204 | 4/4 | 12/12 | 100.0% | 12 | 0 | 0 | 0 | 100.0% | 4/4 | 12 | 273.22 | 522.88 |
| 台湾 | https://cp.cloudflare.com/generate\_204 | 10/10 | 30/30 | 100.0% | 30 | 0 | 0 | 0 | 100.0% | 10/10 | 30 | 276.12 | 537.26 |
| 台湾 | https://www.gstatic.com/generate\_204 | 10/10 | 30/30 | 100.0% | 30 | 0 | 0 | 0 | 100.0% | 10/10 | 30 | 266.05 | 502.87 |
| 美国 | https://cp.cloudflare.com/generate\_204 | 13/13 | 39/39 | 100.0% | 39 | 0 | 0 | 0 | 100.0% | 13/13 | 39 | 938.29 | 1239.83 |
| 美国 | https://www.gstatic.com/generate\_204 | 13/13 | 39/39 | 100.0% | 39 | 0 | 0 | 0 | 100.0% | 13/13 | 39 | 771.73 | 1083.54 |

## 各地区节点与目标

| 地区 | 机场 | 节点 | 协议 | 类型 | 目标 | 样本/计划 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 有效数值数 | p50 ms | p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 香港 | amy | amy-19e94a2b074b-16be9c0e42cc | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 193.14 | 446.38 |
| 香港 | amy | amy-19e94a2b074b-16be9c0e42cc | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 247.19 | 424.01 |
| 香港 | amy | amy-1c99303d928e-a7ddc45206c8 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 236.29 | 455.02 |
| 香港 | amy | amy-1c99303d928e-a7ddc45206c8 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 214.97 | 436.19 |
| 香港 | amy | amy-23da1576894b-a7ac33f39360 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 215.17 | 371.23 |
| 香港 | amy | amy-23da1576894b-a7ac33f39360 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 214.98 | 395.00 |
| 香港 | amy | amy-328208001144-8aef33d1bc08 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 215.92 | 407.48 |
| 香港 | amy | amy-328208001144-8aef33d1bc08 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 194.32 | 419.19 |
| 香港 | amy | amy-41e16e7c792e-a0b2dc4a0730 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 215.81 | 432.95 |
| 香港 | amy | amy-41e16e7c792e-a0b2dc4a0730 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 209.21 | 434.03 |
| 香港 | amy | amy-4852919c4de5-236e6637384c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 234.84 | 665.34 |
| 香港 | amy | amy-4852919c4de5-236e6637384c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 223.83 | 644.65 |
| 香港 | amy | amy-487bfe63a897-303fc0b89212 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 213.90 | 411.03 |
| 香港 | amy | amy-487bfe63a897-303fc0b89212 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 514.01 | 536.21 |
| 香港 | amy | amy-5db6a464ff63-4558d99289a6 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 218.21 | 474.67 |
| 香港 | amy | amy-5db6a464ff63-4558d99289a6 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 311.87 | 502.19 |
| 香港 | amy | amy-627234b682bd-b15d2547a14c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 238.15 | 449.10 |
| 香港 | amy | amy-627234b682bd-b15d2547a14c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 227.60 | 405.90 |
| 香港 | amy | amy-6862e449e461-2b1ae5991847 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 218.48 | 653.05 |
| 香港 | amy | amy-6862e449e461-2b1ae5991847 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 244.46 | 641.81 |
| 香港 | amy | amy-7e6270835dbe-9c6e4aa0d65c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 227.36 | 457.84 |
| 香港 | amy | amy-7e6270835dbe-9c6e4aa0d65c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 214.99 | 411.03 |
| 香港 | amy | amy-80a470c7b2a0-6c0779bc41ca | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 549.06 | 729.24 |
| 香港 | amy | amy-80a470c7b2a0-6c0779bc41ca | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 229.66 | 405.92 |
| 香港 | amy | amy-9d3e125fb231-b0d6bc2e2513 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 221.70 | 432.51 |
| 香港 | amy | amy-9d3e125fb231-b0d6bc2e2513 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 211.27 | 466.59 |
| 香港 | amy | amy-a09c6020552c-1634ec436acd | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 183.79 | 449.24 |
| 香港 | amy | amy-a09c6020552c-1634ec436acd | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 186.35 | 441.25 |
| 香港 | amy | amy-a239fbdc06c7-b4143722109c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 243.95 | 448.28 |
| 香港 | amy | amy-a239fbdc06c7-b4143722109c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 324.42 | 464.30 |
| 香港 | amy | amy-ad3174b61150-18abcdd1834a | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 209.19 | 432.06 |
| 香港 | amy | amy-ad3174b61150-18abcdd1834a | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 231.81 | 435.44 |
| 香港 | amy | amy-b3d9af4a307f-6b1c3b31ed46 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 218.75 | 492.19 |
| 香港 | amy | amy-b3d9af4a307f-6b1c3b31ed46 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 238.25 | 505.02 |
| 香港 | amy | amy-b586e3457e9a-40129cf87af7 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 204.38 | 384.42 |
| 香港 | amy | amy-b586e3457e9a-40129cf87af7 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 195.83 | 414.60 |
| 香港 | amy | amy-d700f4e7e188-445a957b290a | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 231.38 | 469.48 |
| 香港 | amy | amy-d700f4e7e188-445a957b290a | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 258.17 | 464.24 |
| 香港 | amy | amy-efc2d3f6aea6-79180d24976f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 197.19 | 407.48 |
| 香港 | amy | amy-efc2d3f6aea6-79180d24976f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 202.27 | 418.11 |
| 香港 | amy | amy-f2a18086c6f8-62bb72ac02cb | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 425.36 | 531.25 |
| 香港 | amy | amy-f2a18086c6f8-62bb72ac02cb | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 275.98 | 478.06 |
| 日本 | amy | amy-0f89aeb95236-55c6a2855b30 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 437.36 | 477.44 |
| 日本 | amy | amy-0f89aeb95236-55c6a2855b30 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 424.15 | 474.43 |
| 日本 | amy | amy-28894fa8df87-f556311b9b2c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 253.03 | 444.02 |
| 日本 | amy | amy-28894fa8df87-f556311b9b2c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 271.12 | 460.16 |
| 日本 | amy | amy-3d4a9f512657-15c5c670f079 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 414.26 | 969.03 |
| 日本 | amy | amy-3d4a9f512657-15c5c670f079 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 383.06 | 494.26 |
| 日本 | amy | amy-46951f246c2d-16c08d01365e | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 249.14 | 457.58 |
| 日本 | amy | amy-46951f246c2d-16c08d01365e | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 242.95 | 465.35 |
| 日本 | amy | amy-530735ac817f-b90a3ea726d7 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 233.33 | 457.00 |
| 日本 | amy | amy-530735ac817f-b90a3ea726d7 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 205.36 | 452.66 |
| 日本 | amy | amy-561c28513aff-990d317b3906 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 223.15 | 446.30 |
| 日本 | amy | amy-561c28513aff-990d317b3906 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 228.58 | 513.05 |
| 日本 | amy | amy-b76dcbebb1f6-1bad8320df7e | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 342.03 | 493.93 |
| 日本 | amy | amy-b76dcbebb1f6-1bad8320df7e | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 346.51 | 504.70 |
| 日本 | amy | amy-ccfa96fc1b6d-3679b86f388d | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 478.63 | 507.62 |
| 日本 | amy | amy-ccfa96fc1b6d-3679b86f388d | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 382.11 | 431.60 |
| 新加坡 | amy | amy-0978809a88f7-eba543e15b79 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 268.25 | 489.75 |
| 新加坡 | amy | amy-0978809a88f7-eba543e15b79 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 278.91 | 492.85 |
| 新加坡 | amy | amy-103e1da7aad0-806a470ae1a9 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 285.80 | 461.63 |
| 新加坡 | amy | amy-103e1da7aad0-806a470ae1a9 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 279.60 | 478.90 |
| 新加坡 | amy | amy-15ccc6a594b8-f63edcd31d79 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 277.99 | 502.83 |
| 新加坡 | amy | amy-15ccc6a594b8-f63edcd31d79 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 265.62 | 472.22 |
| 新加坡 | amy | amy-c2b7239d25d2-c8dc143890a8 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 302.06 | 519.50 |
| 新加坡 | amy | amy-c2b7239d25d2-c8dc143890a8 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 267.53 | 504.23 |
| 台湾 | amy | amy-18138e47e4d3-adbd6d37d6fe | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 263.67 | 462.94 |
| 台湾 | amy | amy-18138e47e4d3-adbd6d37d6fe | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 232.70 | 451.30 |
| 台湾 | amy | amy-182c1c20a6a0-9ac167ced453 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 235.08 | 459.62 |
| 台湾 | amy | amy-182c1c20a6a0-9ac167ced453 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 259.23 | 417.90 |
| 台湾 | amy | amy-26d2d6123ab1-22e4a275dbf9 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 457.50 | 497.48 |
| 台湾 | amy | amy-26d2d6123ab1-22e4a275dbf9 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 457.52 | 492.58 |
| 台湾 | amy | amy-502fb418247f-d3308dbba751 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 277.67 | 492.33 |
| 台湾 | amy | amy-502fb418247f-d3308dbba751 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 234.71 | 480.76 |
| 台湾 | amy | amy-69fa0492742d-27c8d50e6783 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 491.42 | 615.75 |
| 台湾 | amy | amy-69fa0492742d-27c8d50e6783 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 267.73 | 488.44 |
| 台湾 | amy | amy-976d0d23f6d6-969b5dd62b35 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 269.26 | 476.27 |
| 台湾 | amy | amy-976d0d23f6d6-969b5dd62b35 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 226.02 | 437.09 |
| 台湾 | amy | amy-aa4eda413954-7a4f09e986e7 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 274.46 | 516.18 |
| 台湾 | amy | amy-aa4eda413954-7a4f09e986e7 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 273.12 | 473.99 |
| 台湾 | amy | amy-c66e324ab73d-f778361ca730 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 278.81 | 474.40 |
| 台湾 | amy | amy-c66e324ab73d-f778361ca730 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 295.55 | 419.69 |
| 台湾 | amy | amy-df86ed92863f-10738796e4fe | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 279.16 | 505.10 |
| 台湾 | amy | amy-df86ed92863f-10738796e4fe | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 239.41 | 455.39 |
| 台湾 | amy | amy-f40aeca0915b-b2450d5fc875 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 274.57 | 479.67 |
| 台湾 | amy | amy-f40aeca0915b-b2450d5fc875 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 249.97 | 407.22 |
| 美国 | amy | amy-022ca128229f-109777c94394 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 952.91 | 1099.54 |
| 美国 | amy | amy-022ca128229f-109777c94394 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 898.28 | 1001.18 |
| 美国 | amy | amy-10e7425b2bdf-90133b8cc463 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 919.42 | 1103.60 |
| 美国 | amy | amy-10e7425b2bdf-90133b8cc463 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 771.73 | 938.47 |
| 美国 | amy | amy-67d52d1c913a-4ae548edd2b5 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1170.78 | 1192.41 |
| 美国 | amy | amy-67d52d1c913a-4ae548edd2b5 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 782.00 | 957.89 |
| 美国 | amy | amy-74672d6bd9e1-043e837a7cc5 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 947.79 | 1174.65 |
| 美国 | amy | amy-74672d6bd9e1-043e837a7cc5 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 770.33 | 966.30 |
| 美国 | amy | amy-78f0e11c82e1-1de0d8f4eeaf | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 932.48 | 1159.36 |
| 美国 | amy | amy-78f0e11c82e1-1de0d8f4eeaf | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 751.48 | 1003.40 |
| 美国 | amy | amy-8fea2cd018c5-7ba05af9d3ca | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 897.50 | 1125.97 |
| 美国 | amy | amy-8fea2cd018c5-7ba05af9d3ca | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 779.25 | 964.11 |
| 美国 | amy | amy-9bb53b684d5e-d36ac60f4c7f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1029.44 | 1144.33 |
| 美国 | amy | amy-9bb53b684d5e-d36ac60f4c7f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 764.95 | 971.38 |
| 美国 | amy | amy-a1bb5963304d-ef80a3e43eec | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 950.85 | 1580.41 |
| 美国 | amy | amy-a1bb5963304d-ef80a3e43eec | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 764.85 | 1358.39 |
| 美国 | amy | amy-c6edd85639db-ca19a0d51243 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 938.29 | 1135.34 |
| 美国 | amy | amy-c6edd85639db-ca19a0d51243 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 772.47 | 1018.35 |
| 美国 | amy | amy-d291e6f12f13-1b4bc1fd0396 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 920.94 | 1155.32 |
| 美国 | amy | amy-d291e6f12f13-1b4bc1fd0396 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 843.47 | 1012.42 |
| 美国 | amy | amy-e6e6f902d380-5f7e6efcef90 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 953.38 | 1094.26 |
| 美国 | amy | amy-e6e6f902d380-5f7e6efcef90 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 742.35 | 1000.92 |
| 美国 | amy | amy-f288e3e65023-0bb9dbbc9e56 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 917.63 | 1531.37 |
| 美国 | amy | amy-f288e3e65023-0bb9dbbc9e56 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 763.06 | 1360.07 |
| 美国 | amy | amy-f99b1a0e472d-eadaed2f0e32 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 933.69 | 1155.81 |
| 美国 | amy | amy-f99b1a0e472d-eadaed2f0e32 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 837.92 | 1020.47 |

## 局限

- 本次结果只描述指定时间、测试设备、网络与目标的观测，不代表长期 SLA；短时失败比例不是 ICMP 丢包率。
- 网络路径为 unverified 或 proxy-present 时，不能声称已验证物理直连；WSL 流量也可能经过 Windows 的 TUN 或其他代理。user-confirmed-direct 仅表示用户对路径的确认。interface-bound 仅记录 Mihomo socket 出口接口绑定配置，不表示完整网络路径已审计。
- 本次未测吞吐表现。目标站点、客户端、接入网络与其他流量均会影响结果。
- 地区归类只复述订阅声明，未验证实际出口、运营商或线路类型。同一国家/地区仍可能有不同城市、入口与线路；该分组只减少地区构成差异，不能完全控制线路差异。报告使用匿名节点 ID，私人名称与别名仅留在 private-nodes.json。
- 最快节点由同一批短测样本挑选，节点越多越可能出现偶然好成绩；应在后续独立时段复测，本次全成功资格不等于长期稳定。所设权重体现使用偏好，不是测得的事实或总体服务质量保证。
- 不提供跨地区综合排名或 QoS 总分。加权延迟仍只是同地区同目标的延迟指标。
