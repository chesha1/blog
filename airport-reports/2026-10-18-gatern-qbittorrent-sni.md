# Gatern 机场 qBittorrent WebUI 断连排查记录

2026 年 10 月 18 日，访问自建 qBittorrent WebUI 时，浏览器报 `ERR_CONNECTION_CLOSED`，同域下的 Grafana 正常。服务端检查和对照实验表明：**本次 Gatern 代理路径中，TLS SNI 包含 `torrent` 的测试名称均在握手阶段断连；不含该字符串的对照名称能够访问同一个 qBittorrent 登录页。** 疑似域名关键词过滤误伤，实际关闭连接的设备及规则仍待机场方确认。

本记录供后续补充 [机场测评报告](../source/_posts/airport-review.md) 使用，保存在 Hexo `source/` 之外。它不是 10 月 15 日延迟测评的新增样本，也不自动改变已有评分。

- 记录日期：2026-10-18；下文时间均为北京时间 UTC+8。
- 关键实验窗口：10:44–10:47。
- 状态：已完成排查并准备工单草稿；截至本次记录，用户尚未提供工单提交记录或机场回复。
- 本次操作：只读诊断；未修改代理规则、节点选择、DNS、Cloudflare 配置或服务部署。

## 起因和服务环境

用户最初怀疑 qBittorrent 服务故障，随后提供浏览器错误：“qbittorrent.99010101.xyz 意外终止了连接。ERR_CONNECTION_CLOSED”，并指出 `https://grafana.99010101.xyz/` 可以正常打开。需要区分机场主动断连与自有站点拒绝机场出口 IP。

两个站点都通过 Cloudflare 和 RackNerd 上的 Traefik 对外提供 HTTPS。qBittorrent WebUI 的容器端口为 8080，公网访问走 443；BT 对等连接另用 6881/TCP 和 UDP。本次探针仅访问 HTTPS 页面及 Cloudflare 诊断接口，没有通过机场进行 BT 下载测试。

本机使用 Windows、Clash Party/Mihomo TUN，诊断同时使用 WSL 与 Windows 原生命令。最初 WSL DNS 返回 `198.18.*` Fake-IP，因此不能把清空代理环境变量或 WSL 的“直连”当成绕过 TUN 的证据。10 月 18 日的底层运营商没有单独核实，不沿用 10 月 15 日报告中的中国移动或中国联通标签。

## 排查经过

| 时间 | 检查 | 结果及含义 |
| --- | --- | --- |
| 约 10:29 | SSH 检查 RackNerd、容器和资源 | qBittorrent、Traefik 连续运行约 25 小时；qBittorrent 无容器重启或 OOM；磁盘使用率 52%，没有明显资源耗尽 |
| 约 10:29–10:30 | 容器 WebUI、Traefik 回环域名、exporter | WebUI 均返回 200；指标显示 qBittorrent v5.2.4、4 个种子、连接正常，仍有上传流量 |
| 约 10:30–10:32 | RackNerd、Oracle 访问公网域名 | 使用浏览器 User-Agent 均返回 200 和 qBittorrent 登录页；登录页 CSS、JS 也可获取 |
| 10:32:11 | Windows 绑定物理网卡并固定 Cloudflare IP | 返回 200，标题为 qBittorrent WebUI；同机默认代理路径则在 TLS 阶段 EOF |
| 10:44:38–10:44:39 | 同节点、同目标 IP，交叉改变 SNI 与 HTTP Host | 失败跟随 qBittorrent SNI，而非 HTTP Host；使用 Grafana SNI 可以请求 qBittorrent 页面 |
| 10:45:14 | 单独检查 TLS 1.2 和 TLS 1.3 | qBittorrent SNI 均在收到证书前 EOF，握手读取 0 字节；Grafana SNI 成功 |
| 10:46:04–10:46:05 | 六种 SNI 名称对照 | 含 `torrent` 的三个名称失败，另外三个名称均返回同一个 qBittorrent 登录页 |
| 10:47:00 | 三组成功路径访问 Cloudflare trace | 均显示出口 IP `89.116.88.134`，Cloudflare 机房 `NRT`，`sni=plaintext` |
| 10:47:04 | 物理网卡绑定复核 `torrent`、`bittorrent` SNI | 两者均返回 200 和 qBittorrent 登录页；这组请求到达 Cloudflare `LHR` |

初期使用 Python 默认 User-Agent 请求公网域名，曾得到 Cloudflare HTTP 403、`error code: 1010`；改用 Chrome User-Agent 后，同一服务器访问成功。这是独立的 HTTP 层现象，不能用来解释用户在收到证书前发生的断连。Cloudflare 将 1010 定义为基于浏览器特征的拒绝，见 [官方说明](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/error-1010/)。

## 关键对照实验

SNI 是 TLS ClientHello 中声明的服务器名称，发送时间早于加密连接内的 HTTP Host。把两者分别控制，可以判断差异是否发生于 TLS 握手阶段，见 [Cloudflare 的 SNI 说明](https://www.cloudflare.com/learning/ssl/what-is-sni/)。

实验固定目标 `172.67.160.99:443`、HTTP/1.1 和浏览器 User-Agent。本机路由日志确认测试经过 `Match → 漏网之鱼 → [gatern] JP丨日本2`，没有命中本地 `REJECT`。以下表格中的子域名均属于 `99010101.xyz`。

### SNI 与 HTTP Host 交叉对照

| TLS SNI | HTTP Host | 结果 |
| --- | --- | --- |
| `qbittorrent.99010101.xyz` | `qbittorrent.99010101.xyz` | TLS EOF，无 HTTP 响应 |
| `qbittorrent.99010101.xyz` | `grafana.99010101.xyz` | TLS EOF，无 HTTP 响应 |
| `grafana.99010101.xyz` | `grafana.99010101.xyz` | HTTP 302，跳转 `/login` |
| `grafana.99010101.xyz` | `qbittorrent.99010101.xyz` | HTTP 200，标题 `qBittorrent WebUI` |

成功的交叉请求 CF-RAY 为 `a4c433cb7801a447-NRT`。这里的成功仅表示未登录页面可获取，没有执行 WebUI 登录或管理操作。

TLS 独立检查中，qBittorrent SNI 在 TLS 1.2、TLS 1.3 下均为 `unexpected EOF`、`no peer certificate`，握手读取 0 字节；Grafana SNI 成功协商 TLS 1.3，证书 CN 为 `99010101.xyz`，签发者为 Google Trust Services WE1。

### torrent 字符串对照

这组使用显式 HTTP 代理 `172.25.64.1:7890`，CONNECT 目标始终为上述 Cloudflare IP，计划发送的 HTTP Host 均设置为 `qbittorrent.99010101.xyz`。六次 CONNECT 均返回 `200 Connection established`，之后才进入 TLS 对照；握手失败的三组没有发送 HTTP 请求。

| TLS SNI | 代理路径结果 | 从本机代理连接开始计时 |
| --- | --- | --- |
| `grafana.99010101.xyz` | TLS 1.3，HTTP 200，qBittorrent 登录页 | 0.887 秒 |
| `qbittorrent.99010101.xyz` | TLS `UNEXPECTED_EOF_WHILE_READING` | 0.296 秒 |
| `qbit.99010101.xyz` | TLS 1.3，HTTP 200，qBittorrent 登录页 | 1.081 秒 |
| `torrent.99010101.xyz` | TLS `UNEXPECTED_EOF_WHILE_READING` | 0.239 秒 |
| `bittorrent.99010101.xyz` | TLS `UNEXPECTED_EOF_WHILE_READING` | 0.113 秒 |
| `bt.99010101.xyz` | TLS 1.3，HTTP 200，qBittorrent 登录页 | 0.375 秒 |

这些耗时仅帮助描述断连阶段，不是节点延迟排名。`qbit`、`bt` 等只是指定给 TLS 的测试名称，没有为实验新增 DNS 记录、网站或证书。

### 出口与本机规则核查

10:47 的三组成功 trace 分别使用 Grafana SNI/Grafana Host、Grafana SNI/qBittorrent Host、qbit SNI/qBittorrent Host，均显示出口 `89.116.88.134`、机房 `NRT`。失败连接没有取得 trace，因此只能确认它们选择了同一机场节点，不能把成功样本的出口 IP 直接断言为每一条失败连接的出口。

本机运行配置开启 sniffer，`parse-pure-ip=true`、`override-destination=false`。检查的 29 条规则以及规则集名称中没有 torrent/qbit/p2p 字样；六次探针的实际路由日志均为 Match 并选中日本2节点。没有发现本地规则拒绝这些请求的证据，但未逐项审计所有外部规则集的内容。

初期日志还出现过 `[gatern] JP丨日本3` 和 `[gatern] US丨华盛顿1` 的相关访问。完整的同 IP、SNI、Host 对照只在日本2节点完成，不据此认定所有 Gatern 节点都有相同问题。

### 物理网卡绑定对照

Windows 原生 curl 绑定物理网卡 `192.168.8.100`（Realtek，ifIndex 16），固定相同 Cloudflare IP，HTTP Host 仍为 qBittorrent。`torrent.99010101.xyz`、`bittorrent.99010101.xyz` 两种 SNI 均返回 200 和 qBittorrent 登录页；对应 CF-RAY 为 `a4c437590919e908-LHR`、`a4c43758fee8ada3-LHR`。

这是物理接口绑定对照，未做全链路抓包审计。Cloudflare 使用 Anycast；固定同一个 IP 不代表到达同一边缘机房。本次代理成功样本到达 NRT，物理网卡绑定样本到达 LHR，因此这项对照不能完全排除特定 Cloudflare 边缘的差异。

## 当前判断和证据边界

**已验证的事实**是：服务端正常；本机代理路径的失败发生在 HTTP 之前；固定目标 IP 和 HTTP Host 时，结果随 SNI 名称是否包含 `torrent` 而变化；同一代理路径可以正常取得 qBittorrent 登录页。

**最符合现有现象的解释**是机场或其上游对 SNI 中的 `torrent` 字符串进行了相关处理，可能是防 BT 规则误伤普通 HTTPS 管理页面。这是原因推断，尚不是服务方确认的规则行为。普通的 qBittorrent/Traefik 登录或 HTTP 访问控制，以及对整个机场出口 IP 的统一封禁，都难以解释这组结果。

**尚未定位的部分**是最初发起关闭的设备与规则。没有机场出站日志、双端抓包或 Cloudflare Security Events，不能写成“已经证实机场主动封禁”，也不能完全排除 Cloudflare 边缘或其他中间环节的行为。此次是一个短时、单节点的受控样本，没有测故障发生率、持续时间或全机场覆盖范围。

## 工单草稿

标题：疑似 torrent 域名关键词过滤误伤 HTTPS 管理页面

> 北京时间 2026-10-18 10:44–10:47，使用「JP丨日本2」节点访问 `https://qbittorrent.99010101.xyz/`，浏览器报 `ERR_CONNECTION_CLOSED`，但同站点的 Grafana 正常。
>
> 已做固定目标 IP 的对照：连接 Cloudflare `172.67.160.99:443`，HTTP Host 始终为 `qbittorrent.99010101.xyz`。TLS SNI 使用 `grafana`、`qbit`、`bt` 子域名时，均返回 200 和 qBittorrent 登录页；使用 `qbittorrent`、`torrent`、`bittorrent` 子域名时，均在 TLS 握手阶段断连。对实际 qBittorrent 域名，TLS 1.2 和 1.3 均在收到服务器证书之前断开。
>
> 三组成功的 Cloudflare trace 显示出口 IP 为 `89.116.88.134`，机房 NRT。本地代理日志确认探针均选择该节点，没有命中拒绝规则；绑定物理网卡进行相同 SNI 测试可以成功，但这组到达 LHR，尚未排除 Cloudflare 边缘差异。
>
> 该访问是 TCP 443 上的普通 HTTPS WebUI，并非通过机场下载 BT。请协助检查节点及上游是否存在针对 TLS SNI 中 `torrent` 关键词的过滤规则，并确认是否误伤普通 HTTPS 访问。若并非贵方策略，请协助核查对应时间的出站连接关闭原因。

## 后续回复与复测

| 项目 | 当前记录 |
| --- | --- |
| 工单编号及提交时间 | 待用户提供 |
| 首次回复时间及原文 | 待补充 |
| 服务方确认的原因和影响范围 | 待补充，保留原文与日期 |
| 服务方是否调整规则及完成时间 | 待补充 |
| 同节点同参数复测结果 | 待补充，另记出口 IP、Cloudflare 机房和响应阶段 |
| 最终状态 | 原因待服务方确认 |

后续完善测评时，先阅读本记录，再把“本次实测”“机场回复”“修复后复测”分别写清楚。机场表示已修复与实际复测恢复是两件事；如果仅建议改域名或直连，也应如实记录为绕行方案。此前只提出过该 WebUI 域名配置 DIRECT 的建议，未实施或验证该规则变更。

现有测评已经记载过另一次“机房断电”全线断联工单，那次回复和处理时长不属于本事件。没有新的证据时，不把本次推断扩大为所有节点、长期稳定性结论或确定的协议封锁政策。

## 复现方法与证据附件

以下示例在连接同一机场节点的本机执行，假设 HTTP 代理监听 `127.0.0.1:7890`；从 WSL 使用时换成当时实际可达的 Windows 代理地址。固定 IP、代理地址、节点和出口都属于当天快照，复测时重新确认，不把当前网络变化写回历史结果。

```bash
probe_ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'

# qBittorrent SNI，当时在 TLS 阶段断连
curl --proxy http://127.0.0.1:7890 --noproxy '' --http1.1 \
  --connect-timeout 10 --max-time 15 -A "$probe_ua" \
  --connect-to qbittorrent.99010101.xyz:443:172.67.160.99:443 \
  -D - -o /dev/null https://qbittorrent.99010101.xyz/

# Grafana SNI，HTTP Host 仍是 qBittorrent，当时返回登录页
curl --proxy http://127.0.0.1:7890 --noproxy '' --http1.1 \
  --connect-timeout 10 --max-time 15 -A "$probe_ua" \
  --connect-to grafana.99010101.xyz:443:172.67.160.99:443 \
  -H 'Host: qbittorrent.99010101.xyz' \
  -D - -o /dev/null https://grafana.99010101.xyz/
```

使用显式 HTTP 代理时，通过 `--connect-to` 固定 CONNECT 目标；TLS SNI 仍来自 URL。上述命令是供后续使用的等价复现写法，实际六名称实验使用以下存档 Python 探针。TLS SNI 与 HTTP Host 不同的请求只用于诊断，不作为日常访问方案。

本次证据保存在 [同日附件目录](evidence/2026-10-18-gatern-qbittorrent/)。

- [实际使用的六名称探针](evidence/2026-10-18-gatern-qbittorrent/sni-probe.py)：保留当时的代理地址、Chrome User-Agent、目标 IP 和参数；六名称结果整理自现场命令输出，见上表。
- [Cloudflare trace 原始 JSONL](evidence/2026-10-18-gatern-qbittorrent/cf-trace.jsonl)：三组成功对照的时间、出口 IP、机房、TLS 和 CF-RAY。
- [Mihomo 路由日志摘录](evidence/2026-10-18-gatern-qbittorrent/mihomo-route-excerpts.txt)：仅摘录本次相关目标与时间窗，保留原日志行号。
- [Grafana SNI 请求 qBittorrent 的响应头](evidence/2026-10-18-gatern-qbittorrent/grafana-sni-qbittorrent-host.headers)：10:44 的 HTTP 200 原始响应头。

日志原位置为 Windows `AppData/Roaming/mihomo-party/logs/core-2026-10-18.log`。附件只保留相关诊断内容，不复制订阅、账户口令、完整运行配置或其他浏览记录。
