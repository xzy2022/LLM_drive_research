# 指定 SSH 会话经本机 Wi-Fi 下载

已实现 [Connect-ServerWifi.ps1](../../ai_read/scripts/Connect-ServerWifi.ps1)。用法见 [服务器使用](../../docs/服务器使用.md)。父项目未提交；整理时 HEAD 为 `9ff8a4ea805227460acf02bd98b2081b36fb7b82`，不是本次脚本的提交。最终脚本 SHA-256：`57277BDB0C490EC5855F2C8DAF8D2140D4CF20724636348DCC288C567C3286C0`。

## 人工复核理解

Mihomo Meta 只是复用它的代理程序，省的在本机再写代理程序了，实际上没有对出网做代理。

## 实现

- 本机复用已安装的 Mihomo Meta v1.19.33（windows amd64），独立进程与运行目录。
- HTTP 入口仅绑定本机回环地址；DIRECT、固定 WLAN、IPv4、独立 DNS；不新增 TUN，不加载现有订阅。
- 使用 `ssh xxx -R ...` 反向转发至服务器回环端口，默认 `18797`。不修改服务器路由或永久代理设置，不要求 sudo。
- 默认打开交互 Bash，或通过 `-Command` 执行非交互 Bash 命令。退出后 finally 停止本次本机代理，SSH 关闭远程转发。端口冲突立即失败，不运行目标命令。

## 实测

| 检查 | 结果 |
| --- | --- |
| 服务器通过代理 HTTPS 请求 | 成功；Wi-Fi 公网 IPv4 实测为 `116.162.236.12` / `116.162.236.204`，会变化 |
| PyPI vLLM 索引 | 返回 HTTP 200；没有下载或安装 vLLM |
| 实际小文件下载 | 下载 `idna-3.20-py3-none-any.whl`，69,583 字节；SHA-256 与 PyPI 元数据一致 |
| wheel SHA-256 | `ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c` |
| 物理接口证据 | 独立代理外连源地址 `xxx`；预检曾捕获至 `104.16.124.96:443` 的 Established 连接，正式脚本再次捕获该 WLAN 源地址的 SynSent 连接，见日志 |
| 交互终端 | 服务器真实 PTY、原有 Conda `(base)`、临时 https_proxy、Python 与 exit 均正常 |
| 远程失败命令 | `exit 37` 原样返回 37；本次代理被清理 |
| 远程端口冲突 | 使用已经被现有服务占用的 7001，SSH 返回 255；目标命令未运行，现有服务不受改动 |
| 最终默认状态 | 服务器默认路由仍为 `10.42.0.1/ens111f0`；普通 SSH 无 HTTP/HTTPS/ALL_PROXY；默认 IPv4 出口仍为 `223.104.136.204` |
| 清理 | 所有测试代理进程均已停止，服务器 18797 / 18798 无残留监听 |

机器可读结果见 [verification.json](verification.json)。原始证据在 `logs/`（遵循父项目 gitignore，不自动提交日志）。每次原始代理日志也保留在本机 `%LOCALAPPDATA%\LLM-drive-server-wifi\session-*\`。

## 使用边界

只覆盖支持本次 HTTP 代理设置的程序。没有验证长时间满速下载或断网自动恢复。后台进程／tmux 会保留继承的代理变量；隧道关闭后不会自动改用默认出口。电脑和 Wi-Fi 必须在下载期间保持在线。同一服务器同时打开第二个会话时指定不同的 `-RemotePort`。
