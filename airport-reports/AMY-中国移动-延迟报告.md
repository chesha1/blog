# amy 机场延迟报告

**测试范围：全量节点。** 去重后订阅节点 56 个；本次选中 56 个，有有效记录 56 个，完成全部计划采样 56 个。
**订阅节点覆盖率：100.0%；计划样本覆盖率：100.0%。**节点有记录或采样完成不表示请求成功；成功、失败与无法判定分别统计。
全部去重订阅节点均已完成计划采样。

| 机场 | 订阅原始节点 | 去重节点 | 选中节点 | 有记录节点 | 完整采样节点 | 订阅节点覆盖率 | 有效样本/计划 | 样本覆盖率 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amy | 58 | 56 | 56 | 56 | 56 | 100.0% | 336/336 | 100.0% |

测试时间：2026-10-15T13:27:18.145571+00:00 至 2026-10-15T13:30:13.717323+00:00。状态：completed。
网络路径记录：interface-bound。
网络说明：中国移动移动数据网络（用户确认）；原生 Windows 运行，独立 Mihomo 绑定本机物理以太网接口（ifIndex 14）；宿主 Clash Party TUN 保持开启；已核对接口绑定配置，未做全链路审计。

测试环境：python\_version=3.13.10；system=Windows；release=11；machine=AMD64；is\_wsl=False；mihomo\_version=1.19.31。

计划 336 个样本，有效记录 336 个，覆盖率 100.0%；缺测 0 个。成功 321、失败 15、无法判定 0。

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
- 执行参数：延迟并发 4；延迟按固定批次执行。Mihomo 出口绑定接口：以太网 2；运行总时限 574 秒（来源：automatic）。

## 目标采样与成功计数

| 机场 | 类型 | 目标 | 样本/计划 | 覆盖率 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 节点等权成功率 | 有记录节点/节点 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amy | latency | https://cp.cloudflare.com/generate\_204 | 168/168 | 100.0% | 160 | 8 | 0 | 0 | 95.2% | 95.2% | 56/56 |
| amy | latency | https://www.gstatic.com/generate\_204 | 168/168 | 100.0% | 161 | 7 | 0 | 0 | 95.8% | 95.8% | 56/56 |

总体仅汇总采样与成功计数；延迟按各地区、各目标分别展示。

## 各地区延迟表现

F 为所选最快合格节点在当前目标的 p50，M 为地区各节点成功请求 p50 的中位数，W 为加权延迟。每个地区的各目标使用同一个已通过全部目标资格检查的节点；最快节点 p95 和成功样本/计划数同时列出。p95 只是本次小样本分布的描述。全失败或无合格节点的地区仍保留，无法计算的数值以 — 表示。

| 地区 | 目标 | 所选匿名节点 | 最快 F ms | 最快节点 p95 ms | 最快样本/计划 | 典型 M ms | 加权 W ms | 合格/候选节点 | 资格状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 香港 | https://cp.cloudflare.com/generate\_204 | amy-7e6270835dbe-9c6e4aa0d65c | 243.41 | 272.84 | 3/3 | 276.37 | 250.00 | 21/21 | 已选择 |
| 香港 | https://www.gstatic.com/generate\_204 | amy-7e6270835dbe-9c6e4aa0d65c | 261.96 | 323.60 | 3/3 | 269.10 | 263.39 | 21/21 | 已选择 |
| 日本 | https://cp.cloudflare.com/generate\_204 | amy-ccfa96fc1b6d-3679b86f388d | 1050.07 | 2234.84 | 3/3 | 1089.35 | 1057.93 | 6/8 | 已选择 |
| 日本 | https://www.gstatic.com/generate\_204 | amy-ccfa96fc1b6d-3679b86f388d | 1039.60 | 1245.23 | 3/3 | 1147.29 | 1061.14 | 6/8 | 已选择 |
| 新加坡 | https://cp.cloudflare.com/generate\_204 | amy-0978809a88f7-eba543e15b79 | 327.93 | 345.02 | 3/3 | 338.11 | 329.96 | 4/4 | 已选择 |
| 新加坡 | https://www.gstatic.com/generate\_204 | amy-0978809a88f7-eba543e15b79 | 313.81 | 336.90 | 3/3 | 328.94 | 316.84 | 4/4 | 已选择 |
| 台湾 | https://cp.cloudflare.com/generate\_204 | amy-f40aeca0915b-b2450d5fc875 | 292.09 | 407.10 | 3/3 | 316.64 | 297.00 | 10/10 | 已选择 |
| 台湾 | https://www.gstatic.com/generate\_204 | amy-f40aeca0915b-b2450d5fc875 | 301.73 | 361.14 | 3/3 | 302.29 | 301.84 | 10/10 | 已选择 |
| 美国 | https://cp.cloudflare.com/generate\_204 | amy-c6edd85639db-ca19a0d51243 | 1709.21 | 3703.15 | 3/3 | 1931.04 | 1753.58 | 6/13 | 已选择 |
| 美国 | https://www.gstatic.com/generate\_204 | amy-c6edd85639db-ca19a0d51243 | 1552.29 | 1575.91 | 3/3 | 2236.43 | 1689.11 | 6/13 | 已选择 |

## 各地区采样明细

按地区、目标和测试类型保留全部计划分母。下表的 p50/p95 合并该地区该目标的成功请求，与上表先按节点取中位数的 M 口径不同。地区未知和地区冲突保留采样结果，不选择最快合格节点或计算加权延迟。

| 地区 | 目标 | 有记录节点/计划节点 | 样本/计划 | 覆盖率 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 有数值节点/计划节点 | 有效数值数 | 成功请求 p50 ms | 成功请求 p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 香港 | https://cp.cloudflare.com/generate\_204 | 21/21 | 63/63 | 100.0% | 63 | 0 | 0 | 0 | 100.0% | 21/21 | 63 | 274.54 | 464.27 |
| 香港 | https://www.gstatic.com/generate\_204 | 21/21 | 63/63 | 100.0% | 63 | 0 | 0 | 0 | 100.0% | 21/21 | 63 | 269.10 | 567.28 |
| 日本 | https://cp.cloudflare.com/generate\_204 | 8/8 | 24/24 | 100.0% | 23 | 1 | 0 | 0 | 95.8% | 8/8 | 23 | 1051.54 | 3914.70 |
| 日本 | https://www.gstatic.com/generate\_204 | 8/8 | 24/24 | 100.0% | 23 | 1 | 0 | 0 | 95.8% | 8/8 | 23 | 1233.06 | 2582.51 |
| 新加坡 | https://cp.cloudflare.com/generate\_204 | 4/4 | 12/12 | 100.0% | 12 | 0 | 0 | 0 | 100.0% | 4/4 | 12 | 337.42 | 598.32 |
| 新加坡 | https://www.gstatic.com/generate\_204 | 4/4 | 12/12 | 100.0% | 12 | 0 | 0 | 0 | 100.0% | 4/4 | 12 | 326.64 | 496.79 |
| 台湾 | https://cp.cloudflare.com/generate\_204 | 10/10 | 30/30 | 100.0% | 30 | 0 | 0 | 0 | 100.0% | 10/10 | 30 | 316.64 | 420.21 |
| 台湾 | https://www.gstatic.com/generate\_204 | 10/10 | 30/30 | 100.0% | 30 | 0 | 0 | 0 | 100.0% | 10/10 | 30 | 301.67 | 396.49 |
| 美国 | https://cp.cloudflare.com/generate\_204 | 13/13 | 39/39 | 100.0% | 32 | 7 | 0 | 0 | 82.1% | 13/13 | 32 | 1914.31 | 3929.60 |
| 美国 | https://www.gstatic.com/generate\_204 | 13/13 | 39/39 | 100.0% | 33 | 6 | 0 | 0 | 84.6% | 13/13 | 33 | 1829.34 | 3647.16 |

## 各地区节点与目标

| 地区 | 机场 | 节点 | 协议 | 类型 | 目标 | 样本/计划 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 有效数值数 | p50 ms | p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 香港 | amy | amy-19e94a2b074b-16be9c0e42cc | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 273.36 | 276.15 |
| 香港 | amy | amy-19e94a2b074b-16be9c0e42cc | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 291.92 | 293.19 |
| 香港 | amy | amy-1c99303d928e-a7ddc45206c8 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 276.37 | 303.39 |
| 香港 | amy | amy-1c99303d928e-a7ddc45206c8 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 258.78 | 279.01 |
| 香港 | amy | amy-23da1576894b-a7ac33f39360 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 252.19 | 272.30 |
| 香港 | amy | amy-23da1576894b-a7ac33f39360 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 299.48 | 303.49 |
| 香港 | amy | amy-328208001144-8aef33d1bc08 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 285.65 | 386.98 |
| 香港 | amy | amy-328208001144-8aef33d1bc08 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 285.98 | 335.25 |
| 香港 | amy | amy-41e16e7c792e-a0b2dc4a0730 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 287.12 | 288.59 |
| 香港 | amy | amy-41e16e7c792e-a0b2dc4a0730 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 255.84 | 306.32 |
| 香港 | amy | amy-4852919c4de5-236e6637384c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 299.96 | 452.99 |
| 香港 | amy | amy-4852919c4de5-236e6637384c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 284.49 | 869.58 |
| 香港 | amy | amy-487bfe63a897-303fc0b89212 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 260.57 | 1193.86 |
| 香港 | amy | amy-487bfe63a897-303fc0b89212 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 281.73 | 292.74 |
| 香港 | amy | amy-5db6a464ff63-4558d99289a6 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 267.72 | 283.37 |
| 香港 | amy | amy-5db6a464ff63-4558d99289a6 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 268.92 | 273.50 |
| 香港 | amy | amy-627234b682bd-b15d2547a14c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 281.14 | 349.63 |
| 香港 | amy | amy-627234b682bd-b15d2547a14c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 316.57 | 334.89 |
| 香港 | amy | amy-6862e449e461-2b1ae5991847 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 281.58 | 399.63 |
| 香港 | amy | amy-6862e449e461-2b1ae5991847 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 269.01 | 880.58 |
| 香港 | amy | amy-7e6270835dbe-9c6e4aa0d65c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 243.41 | 272.84 |
| 香港 | amy | amy-7e6270835dbe-9c6e4aa0d65c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 261.96 | 323.60 |
| 香港 | amy | amy-80a470c7b2a0-6c0779bc41ca | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 273.71 | 358.24 |
| 香港 | amy | amy-80a470c7b2a0-6c0779bc41ca | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 310.13 | 794.14 |
| 香港 | amy | amy-9d3e125fb231-b0d6bc2e2513 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 285.25 | 296.00 |
| 香港 | amy | amy-9d3e125fb231-b0d6bc2e2513 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 276.23 | 303.09 |
| 香港 | amy | amy-a09c6020552c-1634ec436acd | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 270.43 | 304.50 |
| 香港 | amy | amy-a09c6020552c-1634ec436acd | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 264.45 | 288.01 |
| 香港 | amy | amy-a239fbdc06c7-b4143722109c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 318.69 | 1117.13 |
| 香港 | amy | amy-a239fbdc06c7-b4143722109c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 260.07 | 285.30 |
| 香港 | amy | amy-ad3174b61150-18abcdd1834a | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 280.00 | 583.79 |
| 香港 | amy | amy-ad3174b61150-18abcdd1834a | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 264.48 | 556.42 |
| 香港 | amy | amy-b3d9af4a307f-6b1c3b31ed46 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 270.63 | 273.61 |
| 香港 | amy | amy-b3d9af4a307f-6b1c3b31ed46 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 253.48 | 354.82 |
| 香港 | amy | amy-b586e3457e9a-40129cf87af7 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 268.78 | 291.57 |
| 香港 | amy | amy-b586e3457e9a-40129cf87af7 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 273.47 | 355.90 |
| 香港 | amy | amy-d700f4e7e188-445a957b290a | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 284.47 | 286.85 |
| 香港 | amy | amy-d700f4e7e188-445a957b290a | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 279.50 | 293.55 |
| 香港 | amy | amy-efc2d3f6aea6-79180d24976f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 275.82 | 275.94 |
| 香港 | amy | amy-efc2d3f6aea6-79180d24976f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 264.80 | 288.81 |
| 香港 | amy | amy-f2a18086c6f8-62bb72ac02cb | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 279.80 | 297.85 |
| 香港 | amy | amy-f2a18086c6f8-62bb72ac02cb | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 269.10 | 362.66 |
| 日本 | amy | amy-0f89aeb95236-55c6a2855b30 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1260.43 | 2920.64 |
| 日本 | amy | amy-0f89aeb95236-55c6a2855b30 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1034.82 | 1233.40 |
| 日本 | amy | amy-28894fa8df87-f556311b9b2c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1991.43 | 3945.27 |
| 日本 | amy | amy-28894fa8df87-f556311b9b2c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 1055.78 | 1532.38 |
| 日本 | amy | amy-3d4a9f512657-15c5c670f079 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1051.54 | 3677.43 |
| 日本 | amy | amy-3d4a9f512657-15c5c670f079 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2301.64 | 3005.25 |
| 日本 | amy | amy-46951f246c2d-16c08d01365e | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1544.52 | 2276.41 |
| 日本 | amy | amy-46951f246c2d-16c08d01365e | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1227.25 | 1252.41 |
| 日本 | amy | amy-530735ac817f-b90a3ea726d7 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1036.46 | 2933.44 |
| 日本 | amy | amy-530735ac817f-b90a3ea726d7 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1538.35 | 2438.34 |
| 日本 | amy | amy-561c28513aff-990d317b3906 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 1127.15 | 1237.37 |
| 日本 | amy | amy-561c28513aff-990d317b3906 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1647.26 | 1755.50 |
| 日本 | amy | amy-b76dcbebb1f6-1bad8320df7e | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1026.98 | 3184.58 |
| 日本 | amy | amy-b76dcbebb1f6-1bad8320df7e | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1067.34 | 2435.41 |
| 日本 | amy | amy-ccfa96fc1b6d-3679b86f388d | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1050.07 | 2234.84 |
| 日本 | amy | amy-ccfa96fc1b6d-3679b86f388d | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1039.60 | 1245.23 |
| 新加坡 | amy | amy-0978809a88f7-eba543e15b79 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 327.93 | 345.02 |
| 新加坡 | amy | amy-0978809a88f7-eba543e15b79 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 313.81 | 336.90 |
| 新加坡 | amy | amy-103e1da7aad0-806a470ae1a9 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 348.28 | 493.96 |
| 新加坡 | amy | amy-103e1da7aad0-806a470ae1a9 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 308.04 | 524.72 |
| 新加坡 | amy | amy-15ccc6a594b8-f63edcd31d79 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 431.90 | 678.67 |
| 新加坡 | amy | amy-15ccc6a594b8-f63edcd31d79 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 372.43 | 446.05 |
| 新加坡 | amy | amy-c2b7239d25d2-c8dc143890a8 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 321.12 | 361.75 |
| 新加坡 | amy | amy-c2b7239d25d2-c8dc143890a8 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 344.07 | 353.85 |
| 台湾 | amy | amy-18138e47e4d3-adbd6d37d6fe | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 319.04 | 349.61 |
| 台湾 | amy | amy-18138e47e4d3-adbd6d37d6fe | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 301.19 | 324.35 |
| 台湾 | amy | amy-182c1c20a6a0-9ac167ced453 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 330.18 | 367.94 |
| 台湾 | amy | amy-182c1c20a6a0-9ac167ced453 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 290.21 | 320.60 |
| 台湾 | amy | amy-26d2d6123ab1-22e4a275dbf9 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 314.55 | 354.02 |
| 台湾 | amy | amy-26d2d6123ab1-22e4a275dbf9 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 292.57 | 300.71 |
| 台湾 | amy | amy-502fb418247f-d3308dbba751 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 308.69 | 338.88 |
| 台湾 | amy | amy-502fb418247f-d3308dbba751 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 312.39 | 340.23 |
| 台湾 | amy | amy-69fa0492742d-27c8d50e6783 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 299.30 | 309.59 |
| 台湾 | amy | amy-69fa0492742d-27c8d50e6783 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 300.59 | 338.41 |
| 台湾 | amy | amy-976d0d23f6d6-969b5dd62b35 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 301.39 | 408.57 |
| 台湾 | amy | amy-976d0d23f6d6-969b5dd62b35 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 327.94 | 410.80 |
| 台湾 | amy | amy-aa4eda413954-7a4f09e986e7 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 341.71 | 842.18 |
| 台湾 | amy | amy-aa4eda413954-7a4f09e986e7 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 315.95 | 440.75 |
| 台湾 | amy | amy-c66e324ab73d-f778361ca730 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 318.74 | 335.22 |
| 台湾 | amy | amy-c66e324ab73d-f778361ca730 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 313.46 | 348.50 |
| 台湾 | amy | amy-df86ed92863f-10738796e4fe | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 321.74 | 332.29 |
| 台湾 | amy | amy-df86ed92863f-10738796e4fe | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 302.86 | 317.00 |
| 台湾 | amy | amy-f40aeca0915b-b2450d5fc875 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 292.09 | 407.10 |
| 台湾 | amy | amy-f40aeca0915b-b2450d5fc875 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 301.73 | 361.14 |
| 美国 | amy | amy-022ca128229f-109777c94394 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 1728.83 | 1739.12 |
| 美国 | amy | amy-022ca128229f-109777c94394 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1742.49 | 1843.18 |
| 美国 | amy | amy-10e7425b2bdf-90133b8cc463 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 3050.14 | 3221.71 |
| 美国 | amy | amy-10e7425b2bdf-90133b8cc463 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2889.37 | 3540.11 |
| 美国 | amy | amy-67d52d1c913a-4ae548edd2b5 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 2168.55 | 2595.23 |
| 美国 | amy | amy-67d52d1c913a-4ae548edd2b5 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 3375.79 | 3517.85 |
| 美国 | amy | amy-74672d6bd9e1-043e837a7cc5 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 2475.21 | 3395.03 |
| 美国 | amy | amy-74672d6bd9e1-043e837a7cc5 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 1424.57 | 1738.24 |
| 美国 | amy | amy-78f0e11c82e1-1de0d8f4eeaf | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1938.34 | 2000.82 |
| 美国 | amy | amy-78f0e11c82e1-1de0d8f4eeaf | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2990.12 | 3628.37 |
| 美国 | amy | amy-8fea2cd018c5-7ba05af9d3ca | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 1831.16 | 1906.01 |
| 美国 | amy | amy-8fea2cd018c5-7ba05af9d3ca | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 1 | 2 | 0 | 0 | 33.3% | 1 | 2967.77 | 2967.77 |
| 美国 | amy | amy-9bb53b684d5e-d36ac60f4c7f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 1551.97 | 1728.68 |
| 美国 | amy | amy-9bb53b684d5e-d36ac60f4c7f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 1308.95 | 1524.87 |
| 美国 | amy | amy-a1bb5963304d-ef80a3e43eec | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1914.29 | 4032.32 |
| 美国 | amy | amy-a1bb5963304d-ef80a3e43eec | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 3097.62 | 3728.70 |
| 美国 | amy | amy-c6edd85639db-ca19a0d51243 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1709.21 | 3703.15 |
| 美国 | amy | amy-c6edd85639db-ca19a0d51243 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1552.29 | 1575.91 |
| 美国 | amy | amy-d291e6f12f13-1b4bc1fd0396 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1937.98 | 3110.24 |
| 美国 | amy | amy-d291e6f12f13-1b4bc1fd0396 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1792.86 | 2764.52 |
| 美国 | amy | amy-e6e6f902d380-5f7e6efcef90 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 1 | 2 | 0 | 0 | 33.3% | 1 | 1931.04 | 1931.04 |
| 美国 | amy | amy-e6e6f902d380-5f7e6efcef90 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2502.36 | 2761.57 |
| 美国 | amy | amy-f288e3e65023-0bb9dbbc9e56 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1715.81 | 3713.61 |
| 美国 | amy | amy-f288e3e65023-0bb9dbbc9e56 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 2236.43 | 2651.89 |
| 美国 | amy | amy-f99b1a0e472d-eadaed2f0e32 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2353.11 | 3603.06 |
| 美国 | amy | amy-f99b1a0e472d-eadaed2f0e32 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1838.01 | 1855.36 |

## 局限

- 本次结果只描述指定时间、测试设备、网络与目标的观测，不代表长期 SLA；短时失败比例不是 ICMP 丢包率。
- 网络路径为 unverified 或 proxy-present 时，不能声称已验证物理直连；WSL 流量也可能经过 Windows 的 TUN 或其他代理。user-confirmed-direct 仅表示用户对路径的确认。interface-bound 仅记录 Mihomo socket 出口接口绑定配置，不表示完整网络路径已审计。
- 本次未测吞吐表现。目标站点、客户端、接入网络与其他流量均会影响结果。
- 地区归类只复述订阅声明，未验证实际出口、运营商或线路类型。同一国家/地区仍可能有不同城市、入口与线路；该分组只减少地区构成差异，不能完全控制线路差异。报告使用匿名节点 ID，私人名称与别名仅留在 private-nodes.json。
- 最快节点由同一批短测样本挑选，节点越多越可能出现偶然好成绩；应在后续独立时段复测，本次全成功资格不等于长期稳定。所设权重体现使用偏好，不是测得的事实或总体服务质量保证。
- 不提供跨地区综合排名或 QoS 总分。加权延迟仍只是同地区同目标的延迟指标。
