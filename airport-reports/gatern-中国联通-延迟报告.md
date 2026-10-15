# gatern 机场延迟报告

**测试范围：全量节点。** 去重后订阅节点 62 个；本次选中 62 个，有有效记录 62 个，完成全部计划采样 62 个。
**订阅节点覆盖率：100.0%；计划样本覆盖率：100.0%。**节点有记录或采样完成不表示请求成功；成功、失败与无法判定分别统计。
全部去重订阅节点均已完成计划采样。

| 机场 | 订阅原始节点 | 去重节点 | 选中节点 | 有记录节点 | 完整采样节点 | 订阅节点覆盖率 | 有效样本/计划 | 样本覆盖率 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gatern | 62 | 62 | 62 | 62 | 62 | 100.0% | 372/372 | 100.0% |

测试时间：2026-10-15T14:13:45.509589+00:00 至 2026-10-15T14:18:21.777173+00:00。状态：completed。
网络路径记录：interface-bound。
网络说明：中国联通流量（用户提供）；Windows 原生运行；物理 WLAN 接口 Up，ifIndex 18，存在默认路由；宿主 Mihomo TUN 开启；独立测试内核绑定 WLAN；未做全链路路径审计。

测试环境：python\_version=3.13.10；system=Windows；release=11；machine=AMD64；is\_wsl=False；mihomo\_version=1.19.31。

计划 372 个样本，有效记录 372 个，覆盖率 100.0%；缺测 0 个。成功 353、失败 19、无法判定 0。

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
- 执行参数：延迟并发 4；延迟按固定批次执行。Mihomo 出口绑定接口：WLAN；运行总时限 904 秒（来源：automatic）。

## 目标采样与成功计数

| 机场 | 类型 | 目标 | 样本/计划 | 覆盖率 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 节点等权成功率 | 有记录节点/节点 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gatern | latency | https://cp.cloudflare.com/generate\_204 | 186/186 | 100.0% | 177 | 9 | 0 | 0 | 95.2% | 95.2% | 62/62 |
| gatern | latency | https://www.gstatic.com/generate\_204 | 186/186 | 100.0% | 176 | 10 | 0 | 0 | 94.6% | 94.6% | 62/62 |

总体仅汇总采样与成功计数；延迟按各地区、各目标分别展示。

## 各地区延迟表现

F 为所选最快合格节点在当前目标的 p50，M 为地区各节点成功请求 p50 的中位数，W 为加权延迟。每个地区的各目标使用同一个已通过全部目标资格检查的节点；最快节点 p95 和成功样本/计划数同时列出。p95 只是本次小样本分布的描述。全失败或无合格节点的地区仍保留，无法计算的数值以 — 表示。

| 地区 | 目标 | 所选匿名节点 | 最快 F ms | 最快节点 p95 ms | 最快样本/计划 | 典型 M ms | 加权 W ms | 合格/候选节点 | 资格状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 阿联酋 | https://cp.cloudflare.com/generate\_204 | gatern-c9a6695349fe-4018d49da98d | 1498.22 | 1524.54 | 3/3 | 1498.22 | 1498.22 | 1/1 | 已选择 |
| 阿联酋 | https://www.gstatic.com/generate\_204 | gatern-c9a6695349fe-4018d49da98d | 1522.12 | 1615.22 | 3/3 | 1522.12 | 1522.12 | 1/1 | 已选择 |
| 阿根廷 | https://cp.cloudflare.com/generate\_204 | gatern-7463fe8ebdfa-4f227ea80182 | 3761.65 | 3898.51 | 3/3 | 3761.65 | 3761.65 | 1/1 | 已选择 |
| 阿根廷 | https://www.gstatic.com/generate\_204 | gatern-7463fe8ebdfa-4f227ea80182 | 2795.20 | 3089.00 | 3/3 | 2795.20 | 2795.20 | 1/1 | 已选择 |
| 澳大利亚 | https://cp.cloudflare.com/generate\_204 | gatern-a03a3ca6809f-982d02522f68 | 805.77 | 871.65 | 3/3 | 856.05 | 815.83 | 2/2 | 已选择 |
| 澳大利亚 | https://www.gstatic.com/generate\_204 | gatern-a03a3ca6809f-982d02522f68 | 1170.90 | 1185.69 | 3/3 | 1208.93 | 1178.51 | 2/2 | 已选择 |
| 巴西 | https://cp.cloudflare.com/generate\_204 | gatern-a34ba96f74fe-7f9a266c813e | 1700.20 | 1709.10 | 3/3 | 1700.20 | 1700.20 | 1/1 | 已选择 |
| 巴西 | https://www.gstatic.com/generate\_204 | gatern-a34ba96f74fe-7f9a266c813e | 1634.95 | 1743.56 | 3/3 | 1634.95 | 1634.95 | 1/1 | 已选择 |
| 加拿大 | https://cp.cloudflare.com/generate\_204 | gatern-c73d1296ef93-f1d3d5a9f1e9 | 1178.67 | 1348.07 | 3/3 | 1178.67 | 1178.67 | 1/1 | 已选择 |
| 加拿大 | https://www.gstatic.com/generate\_204 | gatern-c73d1296ef93-f1d3d5a9f1e9 | 1304.41 | 1539.50 | 3/3 | 1304.41 | 1304.41 | 1/1 | 已选择 |
| 瑞士 | https://cp.cloudflare.com/generate\_204 | gatern-e952b4777c18-30854308d8ec | 1446.69 | 2278.62 | 3/3 | 1446.69 | 1446.69 | 1/1 | 已选择 |
| 瑞士 | https://www.gstatic.com/generate\_204 | gatern-e952b4777c18-30854308d8ec | 1438.85 | 1659.58 | 3/3 | 1438.85 | 1438.85 | 1/1 | 已选择 |
| 德国 | https://cp.cloudflare.com/generate\_204 | gatern-f2fe645438ac-4c58f4597c63 | 1366.30 | 1368.62 | 3/3 | 1366.30 | 1366.30 | 1/1 | 已选择 |
| 德国 | https://www.gstatic.com/generate\_204 | gatern-f2fe645438ac-4c58f4597c63 | 1361.29 | 1368.25 | 3/3 | 1361.29 | 1361.28 | 1/1 | 已选择 |
| 丹麦 | https://cp.cloudflare.com/generate\_204 | gatern-14aabf9306e4-f6b129cf8916 | 1502.86 | 1508.71 | 3/3 | 1502.86 | 1502.86 | 1/1 | 已选择 |
| 丹麦 | https://www.gstatic.com/generate\_204 | gatern-14aabf9306e4-f6b129cf8916 | 1499.04 | 1510.50 | 3/3 | 1499.04 | 1499.04 | 1/1 | 已选择 |
| 埃及 | https://cp.cloudflare.com/generate\_204 | gatern-4e3499b6922d-22a5b30bba5d | 1435.52 | 1534.86 | 3/3 | 1435.52 | 1435.52 | 1/1 | 已选择 |
| 埃及 | https://www.gstatic.com/generate\_204 | gatern-4e3499b6922d-22a5b30bba5d | 1413.16 | 1532.33 | 3/3 | 1413.16 | 1413.16 | 1/1 | 已选择 |
| 法国 | https://cp.cloudflare.com/generate\_204 | gatern-240fb3bdc33d-274b26f8f3fd | 1143.82 | 1506.28 | 3/3 | 1143.82 | 1143.82 | 1/1 | 已选择 |
| 法国 | https://www.gstatic.com/generate\_204 | gatern-240fb3bdc33d-274b26f8f3fd | 1263.53 | 1519.97 | 3/3 | 1263.53 | 1263.53 | 1/1 | 已选择 |
| 英国 | https://cp.cloudflare.com/generate\_204 | gatern-13a9ed660281-246d2a6a3d61 | 1279.36 | 1411.99 | 3/3 | 1391.23 | 1301.73 | 3/3 | 已选择 |
| 英国 | https://www.gstatic.com/generate\_204 | gatern-13a9ed660281-246d2a6a3d61 | 1293.61 | 1301.38 | 3/3 | 1374.51 | 1309.79 | 3/3 | 已选择 |
| 香港 | https://cp.cloudflare.com/generate\_204 | gatern-b12c704af93f-6fdbfae5a84b | 348.38 | 504.64 | 3/3 | 432.13 | 365.13 | 5/5 | 已选择 |
| 香港 | https://www.gstatic.com/generate\_204 | gatern-b12c704af93f-6fdbfae5a84b | 342.95 | 499.03 | 3/3 | 342.95 | 342.95 | 5/5 | 已选择 |
| 印度尼西亚 | https://cp.cloudflare.com/generate\_204 | gatern-fa46a59f6919-99a511d5d8cc | 530.00 | 704.55 | 3/3 | 530.00 | 530.00 | 1/1 | 已选择 |
| 印度尼西亚 | https://www.gstatic.com/generate\_204 | gatern-fa46a59f6919-99a511d5d8cc | 723.95 | 1082.13 | 3/3 | 723.95 | 723.95 | 1/1 | 已选择 |
| 以色列 | https://cp.cloudflare.com/generate\_204 | gatern-dc53834e8114-0c1aa6543093 | 1836.05 | 1910.97 | 3/3 | 1836.05 | 1836.05 | 1/1 | 已选择 |
| 以色列 | https://www.gstatic.com/generate\_204 | gatern-dc53834e8114-0c1aa6543093 | 1610.95 | 1697.65 | 3/3 | 1610.95 | 1610.95 | 1/1 | 已选择 |
| 印度 | https://cp.cloudflare.com/generate\_204 | gatern-fff2828f3f9d-a95b3a1d34bf | 848.04 | 853.76 | 3/3 | 848.04 | 848.04 | 1/1 | 已选择 |
| 印度 | https://www.gstatic.com/generate\_204 | gatern-fff2828f3f9d-a95b3a1d34bf | 674.68 | 964.57 | 3/3 | 674.68 | 674.68 | 1/1 | 已选择 |
| 意大利 | https://cp.cloudflare.com/generate\_204 | gatern-d1fec5ed01d1-415b81832f52 | 1196.98 | 1231.48 | 3/3 | 1196.98 | 1196.98 | 1/1 | 已选择 |
| 意大利 | https://www.gstatic.com/generate\_204 | gatern-d1fec5ed01d1-415b81832f52 | 1186.60 | 2340.94 | 3/3 | 1186.60 | 1186.60 | 1/1 | 已选择 |
| 日本 | https://cp.cloudflare.com/generate\_204 | gatern-291a0dc9e847-5a248aad7f06 | 756.86 | 966.66 | 3/3 | 757.09 | 756.90 | 4/4 | 已选择 |
| 日本 | https://www.gstatic.com/generate\_204 | gatern-291a0dc9e847-5a248aad7f06 | 506.29 | 753.71 | 3/3 | 544.01 | 513.83 | 4/4 | 已选择 |
| 韩国 | https://cp.cloudflare.com/generate\_204 | gatern-82c6a1c36e43-3883def1232f | 467.20 | 566.05 | 3/3 | 467.20 | 467.20 | 3/3 | 已选择 |
| 韩国 | https://www.gstatic.com/generate\_204 | gatern-82c6a1c36e43-3883def1232f | 542.29 | 647.59 | 3/3 | 555.04 | 544.84 | 3/3 | 已选择 |
| 哈萨克斯坦 | https://cp.cloudflare.com/generate\_204 | gatern-03031fc7a979-b690dd074df8 | 1724.55 | 1746.67 | 3/3 | 1724.55 | 1724.55 | 1/1 | 已选择 |
| 哈萨克斯坦 | https://www.gstatic.com/generate\_204 | gatern-03031fc7a979-b690dd074df8 | 2036.31 | 2116.84 | 3/3 | 2036.31 | 2036.31 | 1/1 | 已选择 |
| 立陶宛 | https://cp.cloudflare.com/generate\_204 | gatern-405aae443e63-1b72e0543ec5 | 1491.97 | 1551.28 | 3/3 | 1491.97 | 1491.97 | 1/1 | 已选择 |
| 立陶宛 | https://www.gstatic.com/generate\_204 | gatern-405aae443e63-1b72e0543ec5 | 1529.10 | 1554.87 | 3/3 | 1529.10 | 1529.10 | 1/1 | 已选择 |
| 拉脱维亚 | https://cp.cloudflare.com/generate\_204 | gatern-e7b0c19f4ff4-259542428c41 | 1441.08 | 1537.10 | 3/3 | 1441.08 | 1441.08 | 1/1 | 已选择 |
| 拉脱维亚 | https://www.gstatic.com/generate\_204 | gatern-e7b0c19f4ff4-259542428c41 | 1594.40 | 1611.64 | 3/3 | 1594.40 | 1594.40 | 1/1 | 已选择 |
| 墨西哥 | https://cp.cloudflare.com/generate\_204 | gatern-b9246c9520f2-2de4015a76bf | 1210.11 | 1237.92 | 3/3 | 1210.11 | 1210.11 | 1/1 | 已选择 |
| 墨西哥 | https://www.gstatic.com/generate\_204 | gatern-b9246c9520f2-2de4015a76bf | 1098.48 | 1120.56 | 3/3 | 1098.48 | 1098.48 | 1/1 | 已选择 |
| 马来西亚 | https://cp.cloudflare.com/generate\_204 | gatern-dc282d87256f-01f14589e65e | 1110.28 | 1231.37 | 3/3 | 1110.28 | 1110.28 | 1/1 | 已选择 |
| 马来西亚 | https://www.gstatic.com/generate\_204 | gatern-dc282d87256f-01f14589e65e | 538.64 | 618.95 | 3/3 | 538.64 | 538.64 | 1/1 | 已选择 |
| 尼日利亚 | https://cp.cloudflare.com/generate\_204 | gatern-0db6bcd6d049-c9c14f3deab8 | 1880.72 | 1992.66 | 3/3 | 1880.72 | 1880.72 | 1/1 | 已选择 |
| 尼日利亚 | https://www.gstatic.com/generate\_204 | gatern-0db6bcd6d049-c9c14f3deab8 | 2034.28 | 2081.88 | 3/3 | 2034.28 | 2034.28 | 1/1 | 已选择 |
| 荷兰 | https://cp.cloudflare.com/generate\_204 | gatern-6a54950faef7-3b1bca6b6fa1 | 1306.79 | 1458.93 | 3/3 | 1306.79 | 1306.79 | 1/1 | 已选择 |
| 荷兰 | https://www.gstatic.com/generate\_204 | gatern-6a54950faef7-3b1bca6b6fa1 | 1349.04 | 1448.48 | 3/3 | 1349.04 | 1349.04 | 1/1 | 已选择 |
| 新西兰 | https://cp.cloudflare.com/generate\_204 | gatern-c7d8b5df18f7-26ca6dbc35a9 | 1428.35 | 1525.87 | 3/3 | 1428.35 | 1428.35 | 1/1 | 已选择 |
| 新西兰 | https://www.gstatic.com/generate\_204 | gatern-c7d8b5df18f7-26ca6dbc35a9 | 1883.71 | 1998.07 | 3/3 | 1883.71 | 1883.71 | 1/1 | 已选择 |
| 菲律宾 | https://cp.cloudflare.com/generate\_204 | gatern-edbd29a2522d-aec17641e86c | 676.08 | 766.41 | 3/3 | 676.08 | 676.08 | 1/2 | 已选择 |
| 菲律宾 | https://www.gstatic.com/generate\_204 | gatern-edbd29a2522d-aec17641e86c | 393.58 | 459.74 | 3/3 | 393.58 | 393.58 | 1/2 | 已选择 |
| 巴基斯坦 | https://cp.cloudflare.com/generate\_204 | gatern-29b866276603-e6fca4b3db3b | 1460.98 | 1541.12 | 3/3 | 1460.98 | 1460.98 | 1/1 | 已选择 |
| 巴基斯坦 | https://www.gstatic.com/generate\_204 | gatern-29b866276603-e6fca4b3db3b | 1400.91 | 1672.08 | 3/3 | 1400.91 | 1400.91 | 1/1 | 已选择 |
| 波兰 | https://cp.cloudflare.com/generate\_204 | gatern-14348babc61e-6b4feaa3936f | 1392.13 | 1534.65 | 3/3 | 1392.13 | 1392.13 | 1/1 | 已选择 |
| 波兰 | https://www.gstatic.com/generate\_204 | gatern-14348babc61e-6b4feaa3936f | 1461.02 | 1542.60 | 3/3 | 1461.02 | 1461.02 | 1/1 | 已选择 |
| 罗马尼亚 | https://cp.cloudflare.com/generate\_204 | gatern-e93c0defc630-d9b0e73b9646 | 1511.16 | 1540.06 | 3/3 | 1511.16 | 1511.16 | 1/1 | 已选择 |
| 罗马尼亚 | https://www.gstatic.com/generate\_204 | gatern-e93c0defc630-d9b0e73b9646 | 1528.26 | 1551.40 | 3/3 | 1528.26 | 1528.26 | 1/1 | 已选择 |
| 俄罗斯 | https://cp.cloudflare.com/generate\_204 | gatern-e08bda6d2029-5f4d49b08826 | 1880.79 | 2995.95 | 3/3 | 1880.79 | 1880.79 | 1/1 | 已选择 |
| 俄罗斯 | https://www.gstatic.com/generate\_204 | gatern-e08bda6d2029-5f4d49b08826 | 1777.87 | 1788.56 | 3/3 | 1777.87 | 1777.87 | 1/1 | 已选择 |
| 瑞典 | https://cp.cloudflare.com/generate\_204 | gatern-2623d7e0f862-f99a777607ad | 1370.71 | 1539.60 | 3/3 | 1370.71 | 1370.71 | 1/1 | 已选择 |
| 瑞典 | https://www.gstatic.com/generate\_204 | gatern-2623d7e0f862-f99a777607ad | 1432.01 | 1522.51 | 3/3 | 1432.01 | 1432.01 | 1/1 | 已选择 |
| 新加坡 | https://cp.cloudflare.com/generate\_204 | gatern-550ad4c0e414-a818f34564d1 | 537.98 | 600.43 | 3/3 | 537.98 | 537.98 | 1/3 | 已选择 |
| 新加坡 | https://www.gstatic.com/generate\_204 | gatern-550ad4c0e414-a818f34564d1 | 610.24 | 804.30 | 3/3 | 610.24 | 610.24 | 1/3 | 已选择 |
| 泰国 | https://cp.cloudflare.com/generate\_204 | gatern-9e2ba353fc92-ef7efbf82b7f | 802.00 | 827.74 | 3/3 | 802.00 | 802.00 | 1/1 | 已选择 |
| 泰国 | https://www.gstatic.com/generate\_204 | gatern-9e2ba353fc92-ef7efbf82b7f | 550.87 | 560.44 | 3/3 | 550.87 | 550.87 | 1/1 | 已选择 |
| 土耳其 | https://cp.cloudflare.com/generate\_204 | gatern-3ff86469e71d-8bbe96420a49 | 1496.95 | 1511.85 | 3/3 | 1496.95 | 1496.95 | 1/1 | 已选择 |
| 土耳其 | https://www.gstatic.com/generate\_204 | gatern-3ff86469e71d-8bbe96420a49 | 1513.49 | 1556.86 | 3/3 | 1513.49 | 1513.49 | 1/1 | 已选择 |
| 台湾 | https://cp.cloudflare.com/generate\_204 | gatern-42537e0c3e96-6e066bb596b6 | 497.48 | 699.69 | 3/3 | 545.59 | 507.10 | 3/3 | 已选择 |
| 台湾 | https://www.gstatic.com/generate\_204 | gatern-42537e0c3e96-6e066bb596b6 | 422.94 | 919.35 | 3/3 | 522.64 | 442.88 | 3/3 | 已选择 |
| 乌克兰 | https://cp.cloudflare.com/generate\_204 | gatern-3652d251bf56-7aac6ed32176 | 1413.42 | 1546.10 | 3/3 | 1413.42 | 1413.42 | 1/1 | 已选择 |
| 乌克兰 | https://www.gstatic.com/generate\_204 | gatern-3652d251bf56-7aac6ed32176 | 1470.80 | 1642.80 | 3/3 | 1470.80 | 1470.80 | 1/1 | 已选择 |
| 美国 | https://cp.cloudflare.com/generate\_204 | gatern-b2b1713b62e1-12d02ba7f8a5 | 880.66 | 1010.05 | 3/3 | 1023.39 | 909.20 | 5/6 | 已选择 |
| 美国 | https://www.gstatic.com/generate\_204 | gatern-b2b1713b62e1-12d02ba7f8a5 | 1024.50 | 1024.79 | 3/3 | 1088.27 | 1037.25 | 5/6 | 已选择 |
| 越南 | https://cp.cloudflare.com/generate\_204 | gatern-760b2efe8d15-fdea3c960d37 | 670.48 | 706.11 | 3/3 | 670.48 | 670.47 | 1/1 | 已选择 |
| 越南 | https://www.gstatic.com/generate\_204 | gatern-760b2efe8d15-fdea3c960d37 | 466.28 | 663.86 | 3/3 | 466.28 | 466.28 | 1/1 | 已选择 |
| 南非 | https://cp.cloudflare.com/generate\_204 | gatern-58919b9dea31-cbc1d274e2c2 | 1652.15 | 2060.54 | 3/3 | 1652.15 | 1652.15 | 1/1 | 已选择 |
| 南非 | https://www.gstatic.com/generate\_204 | gatern-58919b9dea31-cbc1d274e2c2 | 2184.03 | 2282.61 | 3/3 | 2184.03 | 2184.03 | 1/1 | 已选择 |

## 各地区采样明细

按地区、目标和测试类型保留全部计划分母。下表的 p50/p95 合并该地区该目标的成功请求，与上表先按节点取中位数的 M 口径不同。地区未知和地区冲突保留采样结果，不选择最快合格节点或计算加权延迟。

| 地区 | 目标 | 有记录节点/计划节点 | 样本/计划 | 覆盖率 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 有数值节点/计划节点 | 有效数值数 | 成功请求 p50 ms | 成功请求 p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 阿联酋 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1498.22 | 1524.54 |
| 阿联酋 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1522.12 | 1615.22 |
| 阿根廷 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 3761.65 | 3898.51 |
| 阿根廷 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2795.20 | 3089.00 |
| 澳大利亚 | https://cp.cloudflare.com/generate\_204 | 2/2 | 6/6 | 100.0% | 6 | 0 | 0 | 0 | 100.0% | 2/2 | 6 | 877.34 | 1063.27 |
| 澳大利亚 | https://www.gstatic.com/generate\_204 | 2/2 | 6/6 | 100.0% | 6 | 0 | 0 | 0 | 100.0% | 2/2 | 6 | 1179.12 | 1265.89 |
| 巴西 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1700.20 | 1709.10 |
| 巴西 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1634.95 | 1743.56 |
| 加拿大 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1178.67 | 1348.07 |
| 加拿大 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1304.41 | 1539.50 |
| 瑞士 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1446.69 | 2278.62 |
| 瑞士 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1438.85 | 1659.58 |
| 德国 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1366.30 | 1368.62 |
| 德国 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1361.29 | 1368.25 |
| 丹麦 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1502.86 | 1508.71 |
| 丹麦 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1499.04 | 1510.50 |
| 埃及 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1435.52 | 1534.86 |
| 埃及 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1413.16 | 1532.33 |
| 法国 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1143.82 | 1506.28 |
| 法国 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1263.53 | 1519.97 |
| 英国 | https://cp.cloudflare.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 1391.23 | 1525.95 |
| 英国 | https://www.gstatic.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 1363.30 | 1499.39 |
| 香港 | https://cp.cloudflare.com/generate\_204 | 5/5 | 15/15 | 100.0% | 15 | 0 | 0 | 0 | 100.0% | 5/5 | 15 | 432.13 | 653.29 |
| 香港 | https://www.gstatic.com/generate\_204 | 5/5 | 15/15 | 100.0% | 15 | 0 | 0 | 0 | 100.0% | 5/5 | 15 | 434.48 | 766.41 |
| 印度尼西亚 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 530.00 | 704.55 |
| 印度尼西亚 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 723.95 | 1082.13 |
| 以色列 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1836.05 | 1910.97 |
| 以色列 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1610.95 | 1697.65 |
| 印度 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 848.04 | 853.76 |
| 印度 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 674.68 | 964.57 |
| 意大利 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1196.98 | 1231.48 |
| 意大利 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1186.60 | 2340.94 |
| 日本 | https://cp.cloudflare.com/generate\_204 | 4/4 | 12/12 | 100.0% | 12 | 0 | 0 | 0 | 100.0% | 4/4 | 12 | 757.09 | 916.29 |
| 日本 | https://www.gstatic.com/generate\_204 | 4/4 | 12/12 | 100.0% | 12 | 0 | 0 | 0 | 100.0% | 4/4 | 12 | 544.01 | 826.31 |
| 韩国 | https://cp.cloudflare.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 467.20 | 681.73 |
| 韩国 | https://www.gstatic.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 573.71 | 832.92 |
| 哈萨克斯坦 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1724.55 | 1746.67 |
| 哈萨克斯坦 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2036.31 | 2116.84 |
| 立陶宛 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1491.97 | 1551.28 |
| 立陶宛 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1529.10 | 1554.87 |
| 拉脱维亚 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1441.08 | 1537.10 |
| 拉脱维亚 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1594.40 | 1611.64 |
| 墨西哥 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1210.11 | 1237.92 |
| 墨西哥 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1098.48 | 1120.56 |
| 马来西亚 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1110.28 | 1231.37 |
| 马来西亚 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 538.64 | 618.95 |
| 尼日利亚 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1880.72 | 1992.66 |
| 尼日利亚 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2034.28 | 2081.88 |
| 荷兰 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1306.79 | 1458.93 |
| 荷兰 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1349.04 | 1448.48 |
| 新西兰 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1428.35 | 1525.87 |
| 新西兰 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1883.71 | 1998.07 |
| 菲律宾 | https://cp.cloudflare.com/generate\_204 | 2/2 | 6/6 | 100.0% | 3 | 3 | 0 | 0 | 50.0% | 1/2 | 3 | 676.08 | 766.41 |
| 菲律宾 | https://www.gstatic.com/generate\_204 | 2/2 | 6/6 | 100.0% | 3 | 3 | 0 | 0 | 50.0% | 1/2 | 3 | 393.58 | 459.74 |
| 巴基斯坦 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1460.98 | 1541.12 |
| 巴基斯坦 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1400.91 | 1672.08 |
| 波兰 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1392.13 | 1534.65 |
| 波兰 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1461.02 | 1542.60 |
| 罗马尼亚 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1511.16 | 1540.06 |
| 罗马尼亚 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1528.26 | 1551.40 |
| 俄罗斯 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1880.79 | 2995.95 |
| 俄罗斯 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1777.87 | 1788.56 |
| 瑞典 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1370.71 | 1539.60 |
| 瑞典 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1432.01 | 1522.51 |
| 新加坡 | https://cp.cloudflare.com/generate\_204 | 3/3 | 9/9 | 100.0% | 3 | 6 | 0 | 0 | 33.3% | 1/3 | 3 | 537.98 | 600.43 |
| 新加坡 | https://www.gstatic.com/generate\_204 | 3/3 | 9/9 | 100.0% | 3 | 6 | 0 | 0 | 33.3% | 1/3 | 3 | 610.24 | 804.30 |
| 泰国 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 802.00 | 827.74 |
| 泰国 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 550.87 | 560.44 |
| 土耳其 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1496.95 | 1511.85 |
| 土耳其 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1513.49 | 1556.86 |
| 台湾 | https://cp.cloudflare.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 545.59 | 694.36 |
| 台湾 | https://www.gstatic.com/generate\_204 | 3/3 | 9/9 | 100.0% | 9 | 0 | 0 | 0 | 100.0% | 3/3 | 9 | 522.64 | 871.06 |
| 乌克兰 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1413.42 | 1546.10 |
| 乌克兰 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1470.80 | 1642.80 |
| 美国 | https://cp.cloudflare.com/generate\_204 | 6/6 | 18/18 | 100.0% | 18 | 0 | 0 | 0 | 100.0% | 6/6 | 18 | 1009.71 | 1375.63 |
| 美国 | https://www.gstatic.com/generate\_204 | 6/6 | 18/18 | 100.0% | 17 | 1 | 0 | 0 | 94.4% | 6/6 | 17 | 1053.46 | 1277.84 |
| 越南 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 670.48 | 706.11 |
| 越南 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 466.28 | 663.86 |
| 南非 | https://cp.cloudflare.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 1652.15 | 2060.54 |
| 南非 | https://www.gstatic.com/generate\_204 | 1/1 | 3/3 | 100.0% | 3 | 0 | 0 | 0 | 100.0% | 1/1 | 3 | 2184.03 | 2282.61 |

## 各地区节点与目标

| 地区 | 机场 | 节点 | 协议 | 类型 | 目标 | 样本/计划 | 成功 | 失败 | 无法判定 | 缺测 | 已观测成功率 | 有效数值数 | p50 ms | p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 阿联酋 | gatern | gatern-c9a6695349fe-4018d49da98d | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1498.22 | 1524.54 |
| 阿联酋 | gatern | gatern-c9a6695349fe-4018d49da98d | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1522.12 | 1615.22 |
| 阿根廷 | gatern | gatern-7463fe8ebdfa-4f227ea80182 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 3761.65 | 3898.51 |
| 阿根廷 | gatern | gatern-7463fe8ebdfa-4f227ea80182 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2795.20 | 3089.00 |
| 澳大利亚 | gatern | gatern-37c8c89fea3d-3c08db71bbd8 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 906.34 | 1094.65 |
| 澳大利亚 | gatern | gatern-37c8c89fea3d-3c08db71bbd8 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1246.96 | 1269.68 |
| 澳大利亚 | gatern | gatern-a03a3ca6809f-982d02522f68 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 805.77 | 871.65 |
| 澳大利亚 | gatern | gatern-a03a3ca6809f-982d02522f68 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1170.90 | 1185.69 |
| 巴西 | gatern | gatern-a34ba96f74fe-7f9a266c813e | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1700.20 | 1709.10 |
| 巴西 | gatern | gatern-a34ba96f74fe-7f9a266c813e | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1634.95 | 1743.56 |
| 加拿大 | gatern | gatern-c73d1296ef93-f1d3d5a9f1e9 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1178.67 | 1348.07 |
| 加拿大 | gatern | gatern-c73d1296ef93-f1d3d5a9f1e9 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1304.41 | 1539.50 |
| 瑞士 | gatern | gatern-e952b4777c18-30854308d8ec | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1446.69 | 2278.62 |
| 瑞士 | gatern | gatern-e952b4777c18-30854308d8ec | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1438.85 | 1659.58 |
| 德国 | gatern | gatern-f2fe645438ac-4c58f4597c63 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1366.30 | 1368.62 |
| 德国 | gatern | gatern-f2fe645438ac-4c58f4597c63 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1361.29 | 1368.25 |
| 丹麦 | gatern | gatern-14aabf9306e4-f6b129cf8916 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1502.86 | 1508.71 |
| 丹麦 | gatern | gatern-14aabf9306e4-f6b129cf8916 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1499.04 | 1510.50 |
| 埃及 | gatern | gatern-4e3499b6922d-22a5b30bba5d | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1435.52 | 1534.86 |
| 埃及 | gatern | gatern-4e3499b6922d-22a5b30bba5d | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1413.16 | 1532.33 |
| 法国 | gatern | gatern-240fb3bdc33d-274b26f8f3fd | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1143.82 | 1506.28 |
| 法国 | gatern | gatern-240fb3bdc33d-274b26f8f3fd | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1263.53 | 1519.97 |
| 英国 | gatern | gatern-13a9ed660281-246d2a6a3d61 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1279.36 | 1411.99 |
| 英国 | gatern | gatern-13a9ed660281-246d2a6a3d61 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1293.61 | 1301.38 |
| 英国 | gatern | gatern-c515beb9b56d-da9ffcce3a14 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1391.23 | 1522.34 |
| 英国 | gatern | gatern-c515beb9b56d-da9ffcce3a14 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1377.69 | 1521.07 |
| 英国 | gatern | gatern-cef954825e7e-4064d993b5a6 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1430.35 | 1501.60 |
| 英国 | gatern | gatern-cef954825e7e-4064d993b5a6 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1374.51 | 1436.12 |
| 香港 | gatern | gatern-22fbe1ced358-a2c11153f27a | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 483.14 | 551.29 |
| 香港 | gatern | gatern-22fbe1ced358-a2c11153f27a | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 319.48 | 543.83 |
| 香港 | gatern | gatern-286c0916cbbd-e2b66d95b321 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 379.37 | 466.27 |
| 香港 | gatern | gatern-286c0916cbbd-e2b66d95b321 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 615.17 | 616.02 |
| 香港 | gatern | gatern-35ea1c0c0cff-199bc2a377a5 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 496.55 | 777.51 |
| 香港 | gatern | gatern-35ea1c0c0cff-199bc2a377a5 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 496.55 | 1055.06 |
| 香港 | gatern | gatern-b12c704af93f-6fdbfae5a84b | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 348.38 | 504.64 |
| 香港 | gatern | gatern-b12c704af93f-6fdbfae5a84b | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 342.95 | 499.03 |
| 香港 | gatern | gatern-f7a068210078-804d0dd9f4fa | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 432.13 | 571.21 |
| 香港 | gatern | gatern-f7a068210078-804d0dd9f4fa | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 328.86 | 558.89 |
| 印度尼西亚 | gatern | gatern-fa46a59f6919-99a511d5d8cc | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 530.00 | 704.55 |
| 印度尼西亚 | gatern | gatern-fa46a59f6919-99a511d5d8cc | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 723.95 | 1082.13 |
| 以色列 | gatern | gatern-dc53834e8114-0c1aa6543093 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1836.05 | 1910.97 |
| 以色列 | gatern | gatern-dc53834e8114-0c1aa6543093 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1610.95 | 1697.65 |
| 印度 | gatern | gatern-fff2828f3f9d-a95b3a1d34bf | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 848.04 | 853.76 |
| 印度 | gatern | gatern-fff2828f3f9d-a95b3a1d34bf | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 674.68 | 964.57 |
| 意大利 | gatern | gatern-d1fec5ed01d1-415b81832f52 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1196.98 | 1231.48 |
| 意大利 | gatern | gatern-d1fec5ed01d1-415b81832f52 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1186.60 | 2340.94 |
| 日本 | gatern | gatern-291a0dc9e847-5a248aad7f06 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 756.86 | 966.66 |
| 日本 | gatern | gatern-291a0dc9e847-5a248aad7f06 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 506.29 | 753.71 |
| 日本 | gatern | gatern-7f17e02a4276-34e0cce45e0b | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 757.33 | 770.77 |
| 日本 | gatern | gatern-7f17e02a4276-34e0cce45e0b | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 561.02 | 629.62 |
| 日本 | gatern | gatern-ec0c18dac1fe-194569d563ff | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 747.81 | 822.23 |
| 日本 | gatern | gatern-ec0c18dac1fe-194569d563ff | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 527.00 | 741.32 |
| 日本 | gatern | gatern-f786f652b81b-ebb23f54a5ab | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 780.52 | 848.45 |
| 日本 | gatern | gatern-f786f652b81b-ebb23f54a5ab | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 609.45 | 854.23 |
| 韩国 | gatern | gatern-0aea178340c1-c987a6a485a4 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 480.86 | 724.46 |
| 韩国 | gatern | gatern-0aea178340c1-c987a6a485a4 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 820.27 | 839.24 |
| 韩国 | gatern | gatern-6a563fdfc4f7-9f8bddbf5fd2 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 461.72 | 486.72 |
| 韩国 | gatern | gatern-6a563fdfc4f7-9f8bddbf5fd2 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 555.04 | 571.84 |
| 韩国 | gatern | gatern-82c6a1c36e43-3883def1232f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 467.20 | 566.05 |
| 韩国 | gatern | gatern-82c6a1c36e43-3883def1232f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 542.29 | 647.59 |
| 哈萨克斯坦 | gatern | gatern-03031fc7a979-b690dd074df8 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1724.55 | 1746.67 |
| 哈萨克斯坦 | gatern | gatern-03031fc7a979-b690dd074df8 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2036.31 | 2116.84 |
| 立陶宛 | gatern | gatern-405aae443e63-1b72e0543ec5 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1491.97 | 1551.28 |
| 立陶宛 | gatern | gatern-405aae443e63-1b72e0543ec5 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1529.10 | 1554.87 |
| 拉脱维亚 | gatern | gatern-e7b0c19f4ff4-259542428c41 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1441.08 | 1537.10 |
| 拉脱维亚 | gatern | gatern-e7b0c19f4ff4-259542428c41 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1594.40 | 1611.64 |
| 墨西哥 | gatern | gatern-b9246c9520f2-2de4015a76bf | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1210.11 | 1237.92 |
| 墨西哥 | gatern | gatern-b9246c9520f2-2de4015a76bf | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1098.48 | 1120.56 |
| 马来西亚 | gatern | gatern-dc282d87256f-01f14589e65e | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1110.28 | 1231.37 |
| 马来西亚 | gatern | gatern-dc282d87256f-01f14589e65e | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 538.64 | 618.95 |
| 尼日利亚 | gatern | gatern-0db6bcd6d049-c9c14f3deab8 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1880.72 | 1992.66 |
| 尼日利亚 | gatern | gatern-0db6bcd6d049-c9c14f3deab8 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2034.28 | 2081.88 |
| 荷兰 | gatern | gatern-6a54950faef7-3b1bca6b6fa1 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1306.79 | 1458.93 |
| 荷兰 | gatern | gatern-6a54950faef7-3b1bca6b6fa1 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1349.04 | 1448.48 |
| 新西兰 | gatern | gatern-c7d8b5df18f7-26ca6dbc35a9 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1428.35 | 1525.87 |
| 新西兰 | gatern | gatern-c7d8b5df18f7-26ca6dbc35a9 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1883.71 | 1998.07 |
| 菲律宾 | gatern | gatern-ac65da269397-11722250c21d | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 菲律宾 | gatern | gatern-ac65da269397-11722250c21d | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 菲律宾 | gatern | gatern-edbd29a2522d-aec17641e86c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 676.08 | 766.41 |
| 菲律宾 | gatern | gatern-edbd29a2522d-aec17641e86c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 393.58 | 459.74 |
| 巴基斯坦 | gatern | gatern-29b866276603-e6fca4b3db3b | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1460.98 | 1541.12 |
| 巴基斯坦 | gatern | gatern-29b866276603-e6fca4b3db3b | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1400.91 | 1672.08 |
| 波兰 | gatern | gatern-14348babc61e-6b4feaa3936f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1392.13 | 1534.65 |
| 波兰 | gatern | gatern-14348babc61e-6b4feaa3936f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1461.02 | 1542.60 |
| 罗马尼亚 | gatern | gatern-e93c0defc630-d9b0e73b9646 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1511.16 | 1540.06 |
| 罗马尼亚 | gatern | gatern-e93c0defc630-d9b0e73b9646 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1528.26 | 1551.40 |
| 俄罗斯 | gatern | gatern-e08bda6d2029-5f4d49b08826 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1880.79 | 2995.95 |
| 俄罗斯 | gatern | gatern-e08bda6d2029-5f4d49b08826 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1777.87 | 1788.56 |
| 瑞典 | gatern | gatern-2623d7e0f862-f99a777607ad | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1370.71 | 1539.60 |
| 瑞典 | gatern | gatern-2623d7e0f862-f99a777607ad | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1432.01 | 1522.51 |
| 新加坡 | gatern | gatern-550ad4c0e414-a818f34564d1 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 537.98 | 600.43 |
| 新加坡 | gatern | gatern-550ad4c0e414-a818f34564d1 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 610.24 | 804.30 |
| 新加坡 | gatern | gatern-847f7abe2877-f572e0b4c7d3 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 新加坡 | gatern | gatern-847f7abe2877-f572e0b4c7d3 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 新加坡 | gatern | gatern-c712c29f4478-fea0b01291ee | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 新加坡 | gatern | gatern-c712c29f4478-fea0b01291ee | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 0 | 3 | 0 | 0 | 0.0% | 0 | — | — |
| 泰国 | gatern | gatern-9e2ba353fc92-ef7efbf82b7f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 802.00 | 827.74 |
| 泰国 | gatern | gatern-9e2ba353fc92-ef7efbf82b7f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 550.87 | 560.44 |
| 土耳其 | gatern | gatern-3ff86469e71d-8bbe96420a49 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1496.95 | 1511.85 |
| 土耳其 | gatern | gatern-3ff86469e71d-8bbe96420a49 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1513.49 | 1556.86 |
| 台湾 | gatern | gatern-0f9df7c71c6c-4fa9afd1201c | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 545.59 | 589.04 |
| 台湾 | gatern | gatern-0f9df7c71c6c-4fa9afd1201c | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 700.21 | 706.09 |
| 台湾 | gatern | gatern-42537e0c3e96-6e066bb596b6 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 497.48 | 699.69 |
| 台湾 | gatern | gatern-42537e0c3e96-6e066bb596b6 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 422.94 | 919.35 |
| 台湾 | gatern | gatern-a805b08f79a6-6d186b762ab6 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 606.61 | 648.07 |
| 台湾 | gatern | gatern-a805b08f79a6-6d186b762ab6 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 522.64 | 696.57 |
| 乌克兰 | gatern | gatern-3652d251bf56-7aac6ed32176 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1413.42 | 1546.10 |
| 乌克兰 | gatern | gatern-3652d251bf56-7aac6ed32176 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1470.80 | 1642.80 |
| 美国 | gatern | gatern-632991bf5ff0-8e4ef3cb0493 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1088.28 | 1204.32 |
| 美国 | gatern | gatern-632991bf5ff0-8e4ef3cb0493 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1106.65 | 1130.87 |
| 美国 | gatern | gatern-78d21b06d871-eece57190b23 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 994.99 | 1186.51 |
| 美国 | gatern | gatern-78d21b06d871-eece57190b23 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1069.88 | 1116.96 |
| 美国 | gatern | gatern-b2b1713b62e1-12d02ba7f8a5 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 880.66 | 1010.05 |
| 美国 | gatern | gatern-b2b1713b62e1-12d02ba7f8a5 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1024.50 | 1024.79 |
| 美国 | gatern | gatern-c433aa034dc0-4f0653d33742 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 940.96 | 1825.80 |
| 美国 | gatern | gatern-c433aa034dc0-4f0653d33742 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 2 | 1 | 0 | 0 | 66.7% | 2 | 790.32 | 1027.15 |
| 美国 | gatern | gatern-f63f5c0722ca-efba85e2322f | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1051.80 | 1256.13 |
| 美国 | gatern | gatern-f63f5c0722ca-efba85e2322f | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1162.49 | 1227.14 |
| 美国 | gatern | gatern-f802caaa150a-705f4d25cc71 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1226.46 | 1260.98 |
| 美国 | gatern | gatern-f802caaa150a-705f4d25cc71 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1144.83 | 1421.20 |
| 越南 | gatern | gatern-760b2efe8d15-fdea3c960d37 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 670.48 | 706.11 |
| 越南 | gatern | gatern-760b2efe8d15-fdea3c960d37 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 466.28 | 663.86 |
| 南非 | gatern | gatern-58919b9dea31-cbc1d274e2c2 | anytls | latency | https://cp.cloudflare.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 1652.15 | 2060.54 |
| 南非 | gatern | gatern-58919b9dea31-cbc1d274e2c2 | anytls | latency | https://www.gstatic.com/generate\_204 | 3/3 | 3 | 0 | 0 | 0 | 100.0% | 3 | 2184.03 | 2282.61 |

## 局限

- 本次结果只描述指定时间、测试设备、网络与目标的观测，不代表长期 SLA；短时失败比例不是 ICMP 丢包率。
- 网络路径为 unverified 或 proxy-present 时，不能声称已验证物理直连；WSL 流量也可能经过 Windows 的 TUN 或其他代理。user-confirmed-direct 仅表示用户对路径的确认。interface-bound 仅记录 Mihomo socket 出口接口绑定配置，不表示完整网络路径已审计。
- 本次未测吞吐表现。目标站点、客户端、接入网络与其他流量均会影响结果。
- 地区归类只复述订阅声明，未验证实际出口、运营商或线路类型。同一国家/地区仍可能有不同城市、入口与线路；该分组只减少地区构成差异，不能完全控制线路差异。报告使用匿名节点 ID，私人名称与别名仅留在 private-nodes.json。
- 最快节点由同一批短测样本挑选，节点越多越可能出现偶然好成绩；应在后续独立时段复测，本次全成功资格不等于长期稳定。所设权重体现使用偏好，不是测得的事实或总体服务质量保证。
- 不提供跨地区综合排名或 QoS 总分。加权延迟仍只是同地区同目标的延迟指标。
