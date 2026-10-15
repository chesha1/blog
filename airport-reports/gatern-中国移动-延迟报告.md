# gatern 机场延迟报告

**测试范围：全量节点。** 去重后订阅节点 62 个；本次选中 62 个，有有效记录 62 个，完成全部计划采样 62 个。
**订阅节点覆盖率：100.0%；计划样本覆盖率：100.0%。**节点有记录或采样完成不表示请求成功；成功、失败与无法判定分别统计。
全部去重订阅节点均已完成计划采样。

| 机场 | 订阅原始节点 | 去重节点 | 选中节点 | 有记录节点 | 完整采样节点 | 订阅节点覆盖率 | 有效样本/计划 | 样本覆盖率 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gatern | 62 | 62 | 62 | 62 | 62 | 100.0% | 372/372 | 100.0% |

测试时间：2026-10-15T13:30:31.243710+00:00 至 2026-10-15T13:35:37.385209+00:00。状态：completed。
网络路径记录：interface-bound。
网络说明：中国移动移动数据网络（用户确认）；原生 Windows 运行，独立 Mihomo 绑定本机物理以太网接口（ifIndex 14）；宿主 Clash Party TUN 保持开启；已核对接口绑定配置，未做全链路审计。

测试环境：python\_version=3.13.10；system=Windows；release=11；machine=AMD64；is\_wsl=False；mihomo\_version=1.19.31。

计划 372 个样本，有效记录 372 个，覆盖率 100.0%；缺测 0 个。成功 354、失败 18、无法判定 0。

原始记录 372 行；排除 0 行。排除原因见数据检查；原始 CSV 保持不变。

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
- 执行参数：延迟并发 4；延迟按固定批次执行。Mihomo 出口绑定接口：以太网 2；运行总时限 904 秒（来源：automatic）。

## 目标采样与成功计数

| 机场 | 类型 | 目标 | 样本/计划 | 覆盖率 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 节点等权成功率 | 有记录节点/节点 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gatern | latency | https://cp.cloudflare.com/generate\_204 | 186/186 | 100.0% | 177 | 9 | 0 | 0 | 95.2% | 95.2% | 62/62 |
| gatern | latency | https://www.gstatic.com/generate\_204 | 186/186 | 100.0% | 177 | 9 | 0 | 0 | 95.2% | 95.2% | 62/62 |

总体仅汇总采样与成功计数；延迟按各地区、各目标分别展示。

## 各地区延迟表现

F 为所选最快合格节点在当前目标的 p50，M 为地区各节点成功请求 p50 的中位数，W 为加权延迟。每个地区的各目标使用同一个已通过全部目标资格检查的节点；最快节点 p95 和成功样本/计划数同时列出。p95 只是本次小样本分布的描述。全失败或无合格节点的地区仍保留，无法计算的数值以 — 表示。

| 地区 | 目标 | 所选匿名节点 | 最快 F ms | 最快节点 p95 ms | 最快样本/计划 | 典型 M ms | 加权 W ms | 合格/候选节点 | 资格状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 阿联酋 | https://cp.cloudflare.com/generate\_204 | gatern-c9a6695349fe-4018d49da98d | 2238.39 | 2245.45 | 3/3 | 2238.39 | 2238.39 | 1/1 | 已选择 |
| 阿联酋 | https://www.gstatic.com/generate\_204 | gatern-c9a6695349fe-4018d49da98d | 1438.93 | 1469.01 | 3/3 | 1438.93 | 1438.93 | 1/1 | 已选择 |
| 阿根廷 | https://cp.cloudflare.com/generate\_204 | gatern-7463fe8ebdfa-4f227ea80182 | 1740.49 | 2356.30 | 3/3 | 1740.49 | 1740.49 | 1/1 | 已选择 |
| 阿根廷 | https://www.gstatic.com/generate\_204 | gatern-7463fe8ebdfa-4f227ea80182 | 1581.68 | 1945.11 | 3/3 | 1581.68 | 1581.68 | 1/1 | 已选择 |
| 澳大利亚 | https://cp.cloudflare.com/generate\_204 | gatern-a03a3ca6809f-982d02522f68 | 765.70 | 1364.67 | 3/3 | 792.28 | 771.01 | 2/2 | 已选择 |
| 澳大利亚 | https://www.gstatic.com/generate\_204 | gatern-a03a3ca6809f-982d02522f68 | 1092.82 | 1461.65 | 3/3 | 1295.21 | 1133.29 | 2/2 | 已选择 |
| 巴西 | https://cp.cloudflare.com/generate\_204 | gatern-a34ba96f74fe-7f9a266c813e | 1516.76 | 2019.85 | 3/3 | 1516.76 | 1516.76 | 1/1 | 已选择 |
| 巴西 | https://www.gstatic.com/generate\_204 | gatern-a34ba96f74fe-7f9a266c813e | 2200.07 | 2299.97 | 3/3 | 2200.07 | 2200.07 | 1/1 | 已选择 |
| 加拿大 | https://cp.cloudflare.com/generate\_204 | gatern-c73d1296ef93-f1d3d5a9f1e9 | 1029.22 | 1473.93 | 3/3 | 1029.22 | 1029.22 | 1/1 | 已选择 |
| 加拿大 | https://www.gstatic.com/generate\_204 | gatern-c73d1296ef93-f1d3d5a9f1e9 | 1547.38 | 1847.51 | 3/3 | 1547.38 | 1547.38 | 1/1 | 已选择 |
| 瑞士 | https://cp.cloudflare.com/generate\_204 | gatern-e952b4777c18-30854308d8ec | 1381.30 | 1828.73 | 3/3 | 1381.30 | 1381.30 | 1/1 | 已选择 |
| 瑞士 | https://www.gstatic.com/generate\_204 | gatern-e952b4777c18-30854308d8ec | 1396.39 | 1858.84 | 3/3 | 1396.39 | 1396.39 | 1/1 | 已选择 |
| 德国 | https://cp.cloudflare.com/generate\_204 | gatern-f2fe645438ac-4c58f4597c63 | 1723.86 | 2023.71 | 3/3 | 1723.86 | 1723.86 | 1/1 | 已选择 |
| 德国 | https://www.gstatic.com/generate\_204 | gatern-f2fe645438ac-4c58f4597c63 | 1303.50 | 1335.87 | 3/3 | 1303.50 | 1303.50 | 1/1 | 已选择 |
| 丹麦 | https://cp.cloudflare.com/generate\_204 | gatern-14aabf9306e4-f6b129cf8916 | 1966.78 | 2001.55 | 3/3 | 1966.78 | 1966.78 | 1/1 | 已选择 |
| 丹麦 | https://www.gstatic.com/generate\_204 | gatern-14aabf9306e4-f6b129cf8916 | 2051.93 | 2064.57 | 3/3 | 2051.93 | 2051.93 | 1/1 | 已选择 |
| 埃及 | https://cp.cloudflare.com/generate\_204 | gatern-4e3499b6922d-22a5b30bba5d | 1254.59 | 1972.71 | 3/3 | 1254.59 | 1254.59 | 1/1 | 已选择 |
| 埃及 | https://www.gstatic.com/generate\_204 | gatern-4e3499b6922d-22a5b30bba5d | 1854.35 | 2008.19 | 3/3 | 1854.35 | 1854.35 | 1/1 | 已选择 |
| 法国 | https://cp.cloudflare.com/generate\_204 | gatern-240fb3bdc33d-274b26f8f3fd | 1041.29 | 1083.91 | 3/3 | 1041.29 | 1041.29 | 1/1 | 已选择 |
| 法国 | https://www.gstatic.com/generate\_204 | gatern-240fb3bdc33d-274b26f8f3fd | 1062.21 | 1225.42 | 3/3 | 1062.21 | 1062.21 | 1/1 | 已选择 |
| 英国 | https://cp.cloudflare.com/generate\_204 | gatern-13a9ed660281-246d2a6a3d61 | 1211.23 | 1285.41 | 3/3 | 1313.42 | 1231.67 | 3/3 | 已选择 |
| 英国 | https://www.gstatic.com/generate\_204 | gatern-13a9ed660281-246d2a6a3d61 | 1235.58 | 1278.31 | 3/3 | 1278.44 | 1244.15 | 3/3 | 已选择 |
| 香港 | https://cp.cloudflare.com/generate\_204 | gatern-35ea1c0c0cff-199bc2a377a5 | 300.00 | 464.91 | 3/3 | 459.07 | 331.82 | 5/5 | 已选择 |
| 香港 | https://www.gstatic.com/generate\_204 | gatern-35ea1c0c0cff-199bc2a377a5 | 417.60 | 1025.39 | 3/3 | 417.60 | 417.60 | 5/5 | 已选择 |
| 印度尼西亚 | https://cp.cloudflare.com/generate\_204 | gatern-fa46a59f6919-99a511d5d8cc | 469.59 | 668.52 | 3/3 | 469.59 | 469.59 | 1/1 | 已选择 |
| 印度尼西亚 | https://www.gstatic.com/generate\_204 | gatern-fa46a59f6919-99a511d5d8cc | 504.72 | 943.38 | 3/3 | 504.72 | 504.72 | 1/1 | 已选择 |
| 以色列 | https://cp.cloudflare.com/generate\_204 | gatern-dc53834e8114-0c1aa6543093 | 2267.38 | 2399.70 | 3/3 | 2267.38 | 2267.38 | 1/1 | 已选择 |
| 以色列 | https://www.gstatic.com/generate\_204 | gatern-dc53834e8114-0c1aa6543093 | 1493.47 | 1594.80 | 3/3 | 1493.47 | 1493.47 | 1/1 | 已选择 |
| 印度 | https://cp.cloudflare.com/generate\_204 | gatern-fff2828f3f9d-a95b3a1d34bf | 785.15 | 790.21 | 3/3 | 785.15 | 785.15 | 1/1 | 已选择 |
| 印度 | https://www.gstatic.com/generate\_204 | gatern-fff2828f3f9d-a95b3a1d34bf | 643.01 | 1091.02 | 3/3 | 643.01 | 643.01 | 1/1 | 已选择 |
| 意大利 | https://cp.cloudflare.com/generate\_204 | gatern-d1fec5ed01d1-415b81832f52 | 1118.15 | 1604.13 | 3/3 | 1118.15 | 1118.15 | 1/1 | 已选择 |
| 意大利 | https://www.gstatic.com/generate\_204 | gatern-d1fec5ed01d1-415b81832f52 | 1095.87 | 1140.82 | 3/3 | 1095.87 | 1095.87 | 1/1 | 已选择 |
| 日本 | https://cp.cloudflare.com/generate\_204 | gatern-291a0dc9e847-5a248aad7f06 | 671.85 | 734.40 | 3/3 | 837.96 | 705.07 | 4/4 | 已选择 |
| 日本 | https://www.gstatic.com/generate\_204 | gatern-291a0dc9e847-5a248aad7f06 | 467.13 | 628.71 | 3/3 | 518.81 | 477.47 | 4/4 | 已选择 |
| 韩国 | https://cp.cloudflare.com/generate\_204 | gatern-82c6a1c36e43-3883def1232f | 417.84 | 436.35 | 3/3 | 431.57 | 420.59 | 3/3 | 已选择 |
| 韩国 | https://www.gstatic.com/generate\_204 | gatern-82c6a1c36e43-3883def1232f | 491.68 | 541.77 | 3/3 | 608.11 | 514.97 | 3/3 | 已选择 |
| 哈萨克斯坦 | https://cp.cloudflare.com/generate\_204 | gatern-03031fc7a979-b690dd074df8 | 2115.73 | 2209.62 | 3/3 | 2115.73 | 2115.73 | 1/1 | 已选择 |
| 哈萨克斯坦 | https://www.gstatic.com/generate\_204 | gatern-03031fc7a979-b690dd074df8 | 2488.91 | 2698.57 | 3/3 | 2488.91 | 2488.91 | 1/1 | 已选择 |
| 立陶宛 | https://cp.cloudflare.com/generate\_204 | gatern-405aae443e63-1b72e0543ec5 | 1369.39 | 1900.76 | 3/3 | 1369.39 | 1369.39 | 1/1 | 已选择 |
| 立陶宛 | https://www.gstatic.com/generate\_204 | gatern-405aae443e63-1b72e0543ec5 | 1404.40 | 1453.91 | 3/3 | 1404.40 | 1404.40 | 1/1 | 已选择 |
| 拉脱维亚 | https://cp.cloudflare.com/generate\_204 | gatern-e7b0c19f4ff4-259542428c41 | 2002.32 | 2231.89 | 3/3 | 2002.32 | 2002.32 | 1/1 | 已选择 |
| 拉脱维亚 | https://www.gstatic.com/generate\_204 | gatern-e7b0c19f4ff4-259542428c41 | 1627.29 | 1963.83 | 3/3 | 1627.29 | 1627.29 | 1/1 | 已选择 |
| 墨西哥 | https://cp.cloudflare.com/generate\_204 | gatern-b9246c9520f2-2de4015a76bf | 996.89 | 1018.50 | 3/3 | 996.89 | 996.89 | 1/1 | 已选择 |
| 墨西哥 | https://www.gstatic.com/generate\_204 | gatern-b9246c9520f2-2de4015a76bf | 1886.23 | 1912.64 | 3/3 | 1886.23 | 1886.23 | 1/1 | 已选择 |
| 马来西亚 | https://cp.cloudflare.com/generate\_204 | gatern-dc282d87256f-01f14589e65e | 802.47 | 1217.01 | 3/3 | 802.47 | 802.47 | 1/1 | 已选择 |
| 马来西亚 | https://www.gstatic.com/generate\_204 | gatern-dc282d87256f-01f14589e65e | 1067.94 | 1154.92 | 3/3 | 1067.94 | 1067.94 | 1/1 | 已选择 |
| 尼日利亚 | https://cp.cloudflare.com/generate\_204 | gatern-0db6bcd6d049-c9c14f3deab8 | 1792.50 | 1894.04 | 3/3 | 1792.50 | 1792.50 | 1/1 | 已选择 |
| 尼日利亚 | https://www.gstatic.com/generate\_204 | gatern-0db6bcd6d049-c9c14f3deab8 | 2065.83 | 2071.55 | 3/3 | 2065.83 | 2065.83 | 1/1 | 已选择 |
| 荷兰 | https://cp.cloudflare.com/generate\_204 | gatern-6a54950faef7-3b1bca6b6fa1 | 1259.12 | 1336.74 | 3/3 | 1259.12 | 1259.12 | 1/1 | 已选择 |
| 荷兰 | https://www.gstatic.com/generate\_204 | gatern-6a54950faef7-3b1bca6b6fa1 | 1306.32 | 1724.65 | 3/3 | 1306.32 | 1306.32 | 1/1 | 已选择 |
| 新西兰 | https://cp.cloudflare.com/generate\_204 | gatern-c7d8b5df18f7-26ca6dbc35a9 | 1384.00 | 1847.38 | 3/3 | 1384.00 | 1384.00 | 1/1 | 已选择 |
| 新西兰 | https://www.gstatic.com/generate\_204 | gatern-c7d8b5df18f7-26ca6dbc35a9 | 2158.77 | 2244.32 | 3/3 | 2158.77 | 2158.77 | 1/1 | 已选择 |
| 菲律宾 | https://cp.cloudflare.com/generate\_204 | gatern-edbd29a2522d-aec17641e86c | 445.30 | 449.68 | 3/3 | 445.30 | 445.30 | 1/2 | 已选择 |
| 菲律宾 | https://www.gstatic.com/generate\_204 | gatern-edbd29a2522d-aec17641e86c | 603.91 | 605.31 | 3/3 | 603.91 | 603.91 | 1/2 | 已选择 |
| 巴基斯坦 | https://cp.cloudflare.com/generate\_204 | gatern-29b866276603-e6fca4b3db3b | 1390.85 | 1504.69 | 3/3 | 1390.85 | 1390.85 | 1/1 | 已选择 |
| 巴基斯坦 | https://www.gstatic.com/generate\_204 | gatern-29b866276603-e6fca4b3db3b | 1063.24 | 1248.36 | 3/3 | 1063.24 | 1063.24 | 1/1 | 已选择 |
| 波兰 | https://cp.cloudflare.com/generate\_204 | gatern-14348babc61e-6b4feaa3936f | 1330.85 | 1834.39 | 3/3 | 1330.85 | 1330.85 | 1/1 | 已选择 |
| 波兰 | https://www.gstatic.com/generate\_204 | gatern-14348babc61e-6b4feaa3936f | 1380.31 | 1913.67 | 3/3 | 1380.31 | 1380.31 | 1/1 | 已选择 |
| 罗马尼亚 | https://cp.cloudflare.com/generate\_204 | gatern-e93c0defc630-d9b0e73b9646 | 1355.27 | 1390.04 | 3/3 | 1355.27 | 1355.27 | 1/1 | 已选择 |
| 罗马尼亚 | https://www.gstatic.com/generate\_204 | gatern-e93c0defc630-d9b0e73b9646 | 1502.34 | 2019.10 | 3/3 | 1502.34 | 1502.34 | 1/1 | 已选择 |
| 俄罗斯 | https://cp.cloudflare.com/generate\_204 | gatern-e08bda6d2029-5f4d49b08826 | 1723.93 | 2203.79 | 3/3 | 1723.93 | 1723.93 | 1/1 | 已选择 |
| 俄罗斯 | https://www.gstatic.com/generate\_204 | gatern-e08bda6d2029-5f4d49b08826 | 1584.11 | 2316.29 | 3/3 | 1584.11 | 1584.11 | 1/1 | 已选择 |
| 瑞典 | https://cp.cloudflare.com/generate\_204 | gatern-2623d7e0f862-f99a777607ad | 1911.62 | 1933.31 | 3/3 | 1911.62 | 1911.62 | 1/1 | 已选择 |
| 瑞典 | https://www.gstatic.com/generate\_204 | gatern-2623d7e0f862-f99a777607ad | 1379.90 | 1472.79 | 3/3 | 1379.90 | 1379.90 | 1/1 | 已选择 |
| 新加坡 | https://cp.cloudflare.com/generate\_204 | gatern-550ad4c0e414-a818f34564d1 | 555.87 | 1180.88 | 3/3 | 555.87 | 555.87 | 1/3 | 已选择 |
| 新加坡 | https://www.gstatic.com/generate\_204 | gatern-550ad4c0e414-a818f34564d1 | 908.52 | 1014.79 | 3/3 | 908.52 | 908.52 | 1/3 | 已选择 |
| 泰国 | https://cp.cloudflare.com/generate\_204 | gatern-9e2ba353fc92-ef7efbf82b7f | 523.80 | 724.73 | 3/3 | 523.80 | 523.80 | 1/1 | 已选择 |
| 泰国 | https://www.gstatic.com/generate\_204 | gatern-9e2ba353fc92-ef7efbf82b7f | 553.24 | 705.84 | 3/3 | 553.24 | 553.24 | 1/1 | 已选择 |
| 土耳其 | https://cp.cloudflare.com/generate\_204 | gatern-3ff86469e71d-8bbe96420a49 | 1451.71 | 1803.80 | 3/3 | 1451.71 | 1451.71 | 1/1 | 已选择 |
| 土耳其 | https://www.gstatic.com/generate\_204 | gatern-3ff86469e71d-8bbe96420a49 | 1416.20 | 2159.81 | 3/3 | 1416.20 | 1416.20 | 1/1 | 已选择 |
| 台湾 | https://cp.cloudflare.com/generate\_204 | gatern-0f9df7c71c6c-4fa9afd1201c | 401.30 | 600.33 | 3/3 | 476.20 | 416.28 | 3/3 | 已选择 |
| 台湾 | https://www.gstatic.com/generate\_204 | gatern-0f9df7c71c6c-4fa9afd1201c | 500.41 | 592.53 | 3/3 | 500.41 | 500.41 | 3/3 | 已选择 |
| 乌克兰 | https://cp.cloudflare.com/generate\_204 | gatern-3652d251bf56-7aac6ed32176 | 1367.43 | 1817.22 | 3/3 | 1367.43 | 1367.43 | 1/1 | 已选择 |
| 乌克兰 | https://www.gstatic.com/generate\_204 | gatern-3652d251bf56-7aac6ed32176 | 1406.00 | 1922.12 | 3/3 | 1406.00 | 1406.00 | 1/1 | 已选择 |
| 美国 | https://cp.cloudflare.com/generate\_204 | gatern-f63f5c0722ca-efba85e2322f | 1017.63 | 1577.84 | 3/3 | 1199.43 | 1053.99 | 6/6 | 已选择 |
| 美国 | https://www.gstatic.com/generate\_204 | gatern-f63f5c0722ca-efba85e2322f | 1084.63 | 1114.08 | 3/3 | 1117.60 | 1091.22 | 6/6 | 已选择 |
| 越南 | https://cp.cloudflare.com/generate\_204 | gatern-760b2efe8d15-fdea3c960d37 | 429.16 | 435.41 | 3/3 | 429.16 | 429.16 | 1/1 | 已选择 |
| 越南 | https://www.gstatic.com/generate\_204 | gatern-760b2efe8d15-fdea3c960d37 | 669.13 | 1175.22 | 3/3 | 669.13 | 669.13 | 1/1 | 已选择 |
| 南非 | https://cp.cloudflare.com/generate\_204 | gatern-58919b9dea31-cbc1d274e2c2 | 1549.08 | 2146.17 | 3/3 | 1549.08 | 1549.08 | 1/1 | 已选择 |
| 南非 | https://www.gstatic.com/generate\_204 | gatern-58919b9dea31-cbc1d274e2c2 | 1955.56 | 2279.96 | 3/3 | 1955.56 | 1955.56 | 1/1 | 已选择 |

## 各地区采样明细

按地区、目标和测试类型保留全部计划分母。下表的 p50/p95 合并该地区该目标的成功请求，与上表先按节点取中位数的 M 口径不同。地区未知和地区冲突保留采样结果，不选择最快合格节点或计算加权延迟。

| 地区 | 目标 | 有记录节点/计划节点 | 样本/计划 | 覆盖率 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 有数值节点/计划节点 | 有效数值数 | 成功请求 p50 ms | 成功请求 p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 阿联酋 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2238.39 | 2245.45 |
| 阿联酋 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1438.93 | 1469.01 |
| 阿根廷 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1740.49 | 2356.30 |
| 阿根廷 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1581.68 | 1945.11 |
| 澳大利亚 | https://cp.cloudflare.com/generate\_204 | 2/2 | 6/6 | 100.0% | 6 | 0 | 0 | 0 | 100.0% | 2/2 | 6 | 804.78 | 1598.66 |
| 澳大利亚 | https://www.gstatic.com/generate\_204 | 2/2 | 6/6 | 100.0% | 6 | 0 | 0 | 0 | 100.0% | 2/2 | 6 | 1470.38 | 1544.40 |
| 巴西 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1516.76 | 2019.85 |
| 巴西 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2200.07 | 2299.97 |
| 加拿大 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1029.22 | 1473.93 |
| 加拿大 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1547.38 | 1847.51 |
| 瑞士 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1381.30 | 1828.73 |
| 瑞士 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1396.39 | 1858.84 |
| 德国 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1723.86 | 2023.71 |
| 德国 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1303.50 | 1335.87 |
| 丹麦 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1966.78 | 2001.55 |
| 丹麦 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2051.93 | 2064.57 |
| 埃及 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1254.59 | 1972.71 |
| 埃及 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1854.35 | 2008.19 |
| 法国 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1041.29 | 1083.91 |
| 法国 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1062.21 | 1225.42 |
| 英国 | https://cp.cloudflare.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 1313.42 | 2014.19 |
| 英国 | https://www.gstatic.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 1283.06 | 1898.54 |
| 香港 | https://cp.cloudflare.com/generate\_204 | 5/5 | 15/15 | 100.0% | 15 | 0 | 0 | 0 | 100.0% | 5/5 | 15 | 459.07 | 949.89 |
| 香港 | https://www.gstatic.com/generate\_204 | 5/5 | 15/15 | 100.0% | 15 | 0 | 0 | 0 | 100.0% | 5/5 | 15 | 417.60 | 1150.19 |
| 印度尼西亚 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 469.59 | 668.52 |
| 印度尼西亚 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 504.72 | 943.38 |
| 以色列 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2267.38 | 2399.70 |
| 以色列 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1493.47 | 1594.80 |
| 印度 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 785.15 | 790.21 |
| 印度 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 643.01 | 1091.02 |
| 意大利 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1118.15 | 1604.13 |
| 意大利 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1095.87 | 1140.82 |
| 日本 | https://cp.cloudflare.com/generate\_204 | 4/4 | 12/12 | 100.0% | 12 | 0 | 0 | 0 | 100.0% | 4/4 | 12 | 741.38 | 1390.15 |
| 日本 | https://www.gstatic.com/generate\_204 | 4/4 | 12/12 | 100.0% | 12 | 0 | 0 | 0 | 100.0% | 4/4 | 12 | 548.24 | 1500.00 |
| 韩国 | https://cp.cloudflare.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 431.57 | 1069.09 |
| 韩国 | https://www.gstatic.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 608.11 | 1290.17 |
| 哈萨克斯坦 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2115.73 | 2209.62 |
| 哈萨克斯坦 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2488.91 | 2698.57 |
| 立陶宛 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1369.39 | 1900.76 |
| 立陶宛 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1404.40 | 1453.91 |
| 拉脱维亚 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2002.32 | 2231.89 |
| 拉脱维亚 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1627.29 | 1963.83 |
| 墨西哥 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 996.89 | 1018.50 |
| 墨西哥 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1886.23 | 1912.64 |
| 马来西亚 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 802.47 | 1217.01 |
| 马来西亚 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1067.94 | 1154.92 |
| 尼日利亚 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1792.50 | 1894.04 |
| 尼日利亚 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2065.83 | 2071.55 |
| 荷兰 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1259.12 | 1336.74 |
| 荷兰 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1306.32 | 1724.65 |
| 新西兰 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1384.00 | 1847.38 |
| 新西兰 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2158.77 | 2244.32 |
| 菲律宾 | https://cp.cloudflare.com/generate\_204 | 2/2 | 6/6 | 100.0% | 3 | 3 | 0 | 0 | 50.0% | 1/2 | 3 | 445.30 | 449.68 |
| 菲律宾 | https://www.gstatic.com/generate\_204 | 2/2 | 6/6 | 100.0% | 3 | 3 | 0 | 0 | 50.0% | 1/2 | 3 | 603.91 | 605.31 |
| 巴基斯坦 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1390.85 | 1504.69 |
| 巴基斯坦 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1063.24 | 1248.36 |
| 波兰 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1330.85 | 1834.39 |
| 波兰 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1380.31 | 1913.67 |
| 罗马尼亚 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1355.27 | 1390.04 |
| 罗马尼亚 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1502.34 | 2019.10 |
| 俄罗斯 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1723.93 | 2203.79 |
| 俄罗斯 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1584.11 | 2316.29 |
| 瑞典 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1911.62 | 1933.31 |
| 瑞典 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1379.90 | 1472.79 |
| 新加坡 | https://cp.cloudflare.com/generate\_204 | 3/3 | 9/9 | 100.0% | 3 | 6 | 0 | 0 | 33.3% | 1/3 | 3 | 555.87 | 1180.88 |
| 新加坡 | https://www.gstatic.com/generate\_204 | 3/3 | 9/9 | 100.0% | 3 | 6 | 0 | 0 | 33.3% | 1/3 | 3 | 908.52 | 1014.79 |
| 泰国 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 523.80 | 724.73 |
| 泰国 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 553.24 | 705.84 |
| 土耳其 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1451.71 | 1803.80 |
| 土耳其 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1416.20 | 2159.81 |
| 台湾 | https://cp.cloudflare.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 560.09 | 815.53 |
| 台湾 | https://www.gstatic.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 385.27 | 913.86 |
| 乌克兰 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1367.43 | 1817.22 |
| 乌克兰 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1406.00 | 1922.12 |
| 美国 | https://cp.cloudflare.com/generate\_204 | 6/6 | 18/18 | 100.0% | 18 | 0 | 0 | 0 | 100.0% | 6/6 | 18 | 1282.81 | 1752.29 |
| 美国 | https://www.gstatic.com/generate\_204 | 6/6 | 18/18 | 100.0% | 18 | 0 | 0 | 0 | 100.0% | 6/6 | 18 | 1110.00 | 1739.08 |
| 越南 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 429.16 | 435.41 |
| 越南 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 669.13 | 1175.22 |
| 南非 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1549.08 | 2146.17 |
| 南非 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1955.56 | 2279.96 |

## 各地区节点与目标

| 地区 | 机场 | 节点 | 协议 | 类型 | 目标 | 样本/计划 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 有效数值数 | p50 ms | p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 阿联酋 | gatern | gatern-c9a6695349fe-4018d49da98d | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2238.39 | 2245.45 |
| 阿联酋 | gatern | gatern-c9a6695349fe-4018d49da98d | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1438.93 | 1469.01 |
| 阿根廷 | gatern | gatern-7463fe8ebdfa-4f227ea80182 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1740.49 | 2356.30 |
| 阿根廷 | gatern | gatern-7463fe8ebdfa-4f227ea80182 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1581.68 | 1945.11 |
| 澳大利亚 | gatern | gatern-37c8c89fea3d-3c08db71bbd8 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 818.87 | 1570.91 |
| 澳大利亚 | gatern | gatern-37c8c89fea3d-3c08db71bbd8 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1497.60 | 1552.25 |
| 澳大利亚 | gatern | gatern-a03a3ca6809f-982d02522f68 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 765.70 | 1364.67 |
| 澳大利亚 | gatern | gatern-a03a3ca6809f-982d02522f68 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1092.82 | 1461.65 |
| 巴西 | gatern | gatern-a34ba96f74fe-7f9a266c813e | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1516.76 | 2019.85 |
| 巴西 | gatern | gatern-a34ba96f74fe-7f9a266c813e | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2200.07 | 2299.97 |
| 加拿大 | gatern | gatern-c73d1296ef93-f1d3d5a9f1e9 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1029.22 | 1473.93 |
| 加拿大 | gatern | gatern-c73d1296ef93-f1d3d5a9f1e9 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1547.38 | 1847.51 |
| 瑞士 | gatern | gatern-e952b4777c18-30854308d8ec | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1381.30 | 1828.73 |
| 瑞士 | gatern | gatern-e952b4777c18-30854308d8ec | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1396.39 | 1858.84 |
| 德国 | gatern | gatern-f2fe645438ac-4c58f4597c63 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1723.86 | 2023.71 |
| 德国 | gatern | gatern-f2fe645438ac-4c58f4597c63 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1303.50 | 1335.87 |
| 丹麦 | gatern | gatern-14aabf9306e4-f6b129cf8916 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1966.78 | 2001.55 |
| 丹麦 | gatern | gatern-14aabf9306e4-f6b129cf8916 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2051.93 | 2064.57 |
| 埃及 | gatern | gatern-4e3499b6922d-22a5b30bba5d | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1254.59 | 1972.71 |
| 埃及 | gatern | gatern-4e3499b6922d-22a5b30bba5d | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1854.35 | 2008.19 |
| 法国 | gatern | gatern-240fb3bdc33d-274b26f8f3fd | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1041.29 | 1083.91 |
| 法国 | gatern | gatern-240fb3bdc33d-274b26f8f3fd | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1062.21 | 1225.42 |
| 英国 | gatern | gatern-13a9ed660281-246d2a6a3d61 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1211.23 | 1285.41 |
| 英国 | gatern | gatern-13a9ed660281-246d2a6a3d61 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1235.58 | 1278.31 |
| 英国 | gatern | gatern-c515beb9b56d-da9ffcce3a14 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1313.42 | 1784.72 |
| 英国 | gatern | gatern-c515beb9b56d-da9ffcce3a14 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1278.44 | 1307.72 |
| 英国 | gatern | gatern-cef954825e7e-4064d993b5a6 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1963.58 | 2039.50 |
| 英国 | gatern | gatern-cef954825e7e-4064d993b5a6 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1763.44 | 1966.10 |
| 香港 | gatern | gatern-22fbe1ced358-a2c11153f27a | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 459.07 | 1047.48 |
| 香港 | gatern | gatern-22fbe1ced358-a2c11153f27a | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 267.44 | 458.58 |
| 香港 | gatern | gatern-286c0916cbbd-e2b66d95b321 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 279.92 | 820.04 |
| 香港 | gatern | gatern-286c0916cbbd-e2b66d95b321 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 493.40 | 846.43 |
| 香港 | gatern | gatern-35ea1c0c0cff-199bc2a377a5 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 300.00 | 464.91 |
| 香港 | gatern | gatern-35ea1c0c0cff-199bc2a377a5 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 417.60 | 1025.39 |
| 香港 | gatern | gatern-b12c704af93f-6fdbfae5a84b | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 784.53 | 867.91 |
| 香港 | gatern | gatern-b12c704af93f-6fdbfae5a84b | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 450.45 | 935.28 |
| 香港 | gatern | gatern-f7a068210078-804d0dd9f4fa | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 493.72 | 709.66 |
| 香港 | gatern | gatern-f7a068210078-804d0dd9f4fa | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 262.58 | 1181.70 |
| 印度尼西亚 | gatern | gatern-fa46a59f6919-99a511d5d8cc | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 469.59 | 668.52 |
| 印度尼西亚 | gatern | gatern-fa46a59f6919-99a511d5d8cc | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 504.72 | 943.38 |
| 以色列 | gatern | gatern-dc53834e8114-0c1aa6543093 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2267.38 | 2399.70 |
| 以色列 | gatern | gatern-dc53834e8114-0c1aa6543093 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1493.47 | 1594.80 |
| 印度 | gatern | gatern-fff2828f3f9d-a95b3a1d34bf | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 785.15 | 790.21 |
| 印度 | gatern | gatern-fff2828f3f9d-a95b3a1d34bf | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 643.01 | 1091.02 |
| 意大利 | gatern | gatern-d1fec5ed01d1-415b81832f52 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1118.15 | 1604.13 |
| 意大利 | gatern | gatern-d1fec5ed01d1-415b81832f52 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1095.87 | 1140.82 |
| 日本 | gatern | gatern-291a0dc9e847-5a248aad7f06 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 671.85 | 734.40 |
| 日本 | gatern | gatern-291a0dc9e847-5a248aad7f06 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 467.13 | 628.71 |
| 日本 | gatern | gatern-7f17e02a4276-34e0cce45e0b | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1268.16 | 1512.14 |
| 日本 | gatern | gatern-7f17e02a4276-34e0cce45e0b | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1261.86 | 1512.92 |
| 日本 | gatern | gatern-ec0c18dac1fe-194569d563ff | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 979.40 | 1064.67 |
| 日本 | gatern | gatern-ec0c18dac1fe-194569d563ff | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 456.14 | 519.00 |
| 日本 | gatern | gatern-f786f652b81b-ebb23f54a5ab | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 696.53 | 932.16 |
| 日本 | gatern | gatern-f786f652b81b-ebb23f54a5ab | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 570.49 | 1377.00 |
| 韩国 | gatern | gatern-0aea178340c1-c987a6a485a4 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 438.01 | 983.77 |
| 韩国 | gatern | gatern-0aea178340c1-c987a6a485a4 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1165.07 | 1352.72 |
| 韩国 | gatern | gatern-6a563fdfc4f7-9f8bddbf5fd2 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 431.57 | 1020.15 |
| 韩国 | gatern | gatern-6a563fdfc4f7-9f8bddbf5fd2 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 608.11 | 632.66 |
| 韩国 | gatern | gatern-82c6a1c36e43-3883def1232f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 417.84 | 436.35 |
| 韩国 | gatern | gatern-82c6a1c36e43-3883def1232f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 491.68 | 541.77 |
| 哈萨克斯坦 | gatern | gatern-03031fc7a979-b690dd074df8 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2115.73 | 2209.62 |
| 哈萨克斯坦 | gatern | gatern-03031fc7a979-b690dd074df8 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2488.91 | 2698.57 |
| 立陶宛 | gatern | gatern-405aae443e63-1b72e0543ec5 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1369.39 | 1900.76 |
| 立陶宛 | gatern | gatern-405aae443e63-1b72e0543ec5 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1404.40 | 1453.91 |
| 拉脱维亚 | gatern | gatern-e7b0c19f4ff4-259542428c41 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2002.32 | 2231.89 |
| 拉脱维亚 | gatern | gatern-e7b0c19f4ff4-259542428c41 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1627.29 | 1963.83 |
| 墨西哥 | gatern | gatern-b9246c9520f2-2de4015a76bf | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 996.89 | 1018.50 |
| 墨西哥 | gatern | gatern-b9246c9520f2-2de4015a76bf | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1886.23 | 1912.64 |
| 马来西亚 | gatern | gatern-dc282d87256f-01f14589e65e | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 802.47 | 1217.01 |
| 马来西亚 | gatern | gatern-dc282d87256f-01f14589e65e | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1067.94 | 1154.92 |
| 尼日利亚 | gatern | gatern-0db6bcd6d049-c9c14f3deab8 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1792.50 | 1894.04 |
| 尼日利亚 | gatern | gatern-0db6bcd6d049-c9c14f3deab8 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2065.83 | 2071.55 |
| 荷兰 | gatern | gatern-6a54950faef7-3b1bca6b6fa1 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1259.12 | 1336.74 |
| 荷兰 | gatern | gatern-6a54950faef7-3b1bca6b6fa1 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1306.32 | 1724.65 |
| 新西兰 | gatern | gatern-c7d8b5df18f7-26ca6dbc35a9 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1384.00 | 1847.38 |
| 新西兰 | gatern | gatern-c7d8b5df18f7-26ca6dbc35a9 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2158.77 | 2244.32 |
| 菲律宾 | gatern | gatern-ac65da269397-11722250c21d | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 菲律宾 | gatern | gatern-ac65da269397-11722250c21d | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 菲律宾 | gatern | gatern-edbd29a2522d-aec17641e86c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 445.30 | 449.68 |
| 菲律宾 | gatern | gatern-edbd29a2522d-aec17641e86c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 603.91 | 605.31 |
| 巴基斯坦 | gatern | gatern-29b866276603-e6fca4b3db3b | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1390.85 | 1504.69 |
| 巴基斯坦 | gatern | gatern-29b866276603-e6fca4b3db3b | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1063.24 | 1248.36 |
| 波兰 | gatern | gatern-14348babc61e-6b4feaa3936f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1330.85 | 1834.39 |
| 波兰 | gatern | gatern-14348babc61e-6b4feaa3936f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1380.31 | 1913.67 |
| 罗马尼亚 | gatern | gatern-e93c0defc630-d9b0e73b9646 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1355.27 | 1390.04 |
| 罗马尼亚 | gatern | gatern-e93c0defc630-d9b0e73b9646 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1502.34 | 2019.10 |
| 俄罗斯 | gatern | gatern-e08bda6d2029-5f4d49b08826 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1723.93 | 2203.79 |
| 俄罗斯 | gatern | gatern-e08bda6d2029-5f4d49b08826 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1584.11 | 2316.29 |
| 瑞典 | gatern | gatern-2623d7e0f862-f99a777607ad | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1911.62 | 1933.31 |
| 瑞典 | gatern | gatern-2623d7e0f862-f99a777607ad | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1379.90 | 1472.79 |
| 新加坡 | gatern | gatern-550ad4c0e414-a818f34564d1 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 555.87 | 1180.88 |
| 新加坡 | gatern | gatern-550ad4c0e414-a818f34564d1 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 908.52 | 1014.79 |
| 新加坡 | gatern | gatern-847f7abe2877-f572e0b4c7d3 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 新加坡 | gatern | gatern-847f7abe2877-f572e0b4c7d3 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 新加坡 | gatern | gatern-c712c29f4478-fea0b01291ee | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 新加坡 | gatern | gatern-c712c29f4478-fea0b01291ee | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 泰国 | gatern | gatern-9e2ba353fc92-ef7efbf82b7f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 523.80 | 724.73 |
| 泰国 | gatern | gatern-9e2ba353fc92-ef7efbf82b7f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 553.24 | 705.84 |
| 土耳其 | gatern | gatern-3ff86469e71d-8bbe96420a49 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1451.71 | 1803.80 |
| 土耳其 | gatern | gatern-3ff86469e71d-8bbe96420a49 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1416.20 | 2159.81 |
| 台湾 | gatern | gatern-0f9df7c71c6c-4fa9afd1201c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 401.30 | 600.33 |
| 台湾 | gatern | gatern-0f9df7c71c6c-4fa9afd1201c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 500.41 | 592.53 |
| 台湾 | gatern | gatern-42537e0c3e96-6e066bb596b6 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 476.20 | 832.97 |
| 台湾 | gatern | gatern-42537e0c3e96-6e066bb596b6 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 649.86 | 1045.86 |
| 台湾 | gatern | gatern-a805b08f79a6-6d186b762ab6 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 726.30 | 729.56 |
| 台湾 | gatern | gatern-a805b08f79a6-6d186b762ab6 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 380.74 | 384.82 |
| 乌克兰 | gatern | gatern-3652d251bf56-7aac6ed32176 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1367.43 | 1817.22 |
| 乌克兰 | gatern | gatern-3652d251bf56-7aac6ed32176 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1406.00 | 1922.12 |
| 美国 | gatern | gatern-632991bf5ff0-8e4ef3cb0493 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1085.87 | 1649.36 |
| 美国 | gatern | gatern-632991bf5ff0-8e4ef3cb0493 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1150.56 | 1492.64 |
| 美国 | gatern | gatern-78d21b06d871-eece57190b23 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1017.74 | 1589.31 |
| 美国 | gatern | gatern-78d21b06d871-eece57190b23 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1527.38 | 1651.24 |
| 美国 | gatern | gatern-b2b1713b62e1-12d02ba7f8a5 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1312.99 | 1472.08 |
| 美国 | gatern | gatern-b2b1713b62e1-12d02ba7f8a5 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 875.90 | 947.73 |
| 美国 | gatern | gatern-c433aa034dc0-4f0653d33742 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1449.59 | 1682.72 |
| 美国 | gatern | gatern-c433aa034dc0-4f0653d33742 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 918.75 | 1026.58 |
| 美国 | gatern | gatern-f63f5c0722ca-efba85e2322f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1017.63 | 1577.84 |
| 美国 | gatern | gatern-f63f5c0722ca-efba85e2322f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1084.63 | 1114.08 |
| 美国 | gatern | gatern-f802caaa150a-705f4d25cc71 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1666.56 | 1949.36 |
| 美国 | gatern | gatern-f802caaa150a-705f4d25cc71 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1734.98 | 1759.61 |
| 越南 | gatern | gatern-760b2efe8d15-fdea3c960d37 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 429.16 | 435.41 |
| 越南 | gatern | gatern-760b2efe8d15-fdea3c960d37 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 669.13 | 1175.22 |
| 南非 | gatern | gatern-58919b9dea31-cbc1d274e2c2 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1549.08 | 2146.17 |
| 南非 | gatern | gatern-58919b9dea31-cbc1d274e2c2 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1955.56 | 2279.96 |

## 局限

- 本次结果只描述指定时间、测试设备、网络与目标的观测，不代表长期 SLA；短时失败比例不是 ICMP 丢包率。
- 网络路径为 unverified 或 proxy-present 时，不能声称已验证物理直连；WSL 流量也可能经过 Windows 的 TUN 或其他代理。user-confirmed-direct 仅表示用户对路径的确认。interface-bound 仅记录 Mihomo socket 出口接口绑定配置，不表示完整网络路径已审计。
- 本次未测吞吐表现。目标站点、客户端、接入网络与其他流量均会影响结果。
- 地区归类只复述订阅声明，未验证实际出口、运营商或线路类型。同一国家/地区仍可能有不同城市、入口与线路；该分组只减少地区构成差异，不能完全控制线路差异。报告使用匿名节点 ID，私人名称与别名仅留在 private-nodes.json。
- 最快节点由同一批短测样本挑选，节点越多越可能出现偶然好成绩；应在后续独立时段复测，本次全成功资格不等于长期稳定。所设权重体现使用偏好，不是测得的事实或总体服务质量保证。
- 不提供跨地区综合排名或 QoS 总分。加权延迟仍只是同地区同目标的延迟指标。
