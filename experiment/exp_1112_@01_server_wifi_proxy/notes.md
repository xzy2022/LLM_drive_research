# 范围与实现记录

- 本次属于服务器联网辅助工具的小规模配置验证，不运行 LaMPilot、不安装 vLLM。
- 只让指定远程命令／交互 shell 使用临时代理；不修改系统默认路由、服务器 shell 启动文件或现有 Clash Verge 配置。
- 复用本机 `C:\Program Files\Clash Verge\verge-mihomo.exe`，单独进程、单独配置目录、仅 DIRECT、固定 WLAN，不启用 TUN。
- SSH 反向转发只绑定服务器回环地址；启动时检查转发失败，退出时清理本次创建的本机进程。
- 工具放在父项目 `scripts/network/`。没有对应的 repos/ 子项目，因此实验原则中的子项目实验分支／合并步骤不适用；不提交或改变父项目现有暂存内容。
- 现有父项目暂存内容：AGENTS.md、docs/服务器使用.md、docs/survey/02a_工具对比与LaMPilot可用性判断.md。保留用户改动。

## 验证中发现并解决的问题

- 初次使用 `mixed-port` 时，一次随机端口在 TCP 可用、UDP 受 Windows 限制的情况下启动失败。工具仅需 HTTP(S) 下载，最终改用 HTTP-only 的 `port`，不再额外创建 SOCKS/UDP 入口。
- 原启动探测的同步 TCP Connect 在无监听时可能等待较久。已改为每次最多等待 250 ms 的异步连接，最多 40 次；HTTPS 检查另有连接和总时限。
- 工具执行器不能创建本机 PowerShell PTY；交互分支改以管道输入命令给本机 pwsh，再由 `ssh -tt` 创建服务器真实 PTY。实际看到原来的 `(base) user@server` 提示符，确认代理变量、Python 命令及 exit 正常。
- DNS 使用独立代理的内部解析器，固定从 WLAN 查询 `223.5.5.5` / `114.114.114.114`；不依赖现有 TUN 的系统 fake-IP 解析。没有修改系统 DNS。
- 请求使用 DIRECT，未加载订阅、代理节点或现有 TUN 配置。实测现有 TUN 开启时，此独立进程的外连源地址为 WLAN 地址。
- 测试期间观察到父项目索引／HEAD 被其他操作更新；本次没有执行 git add、commit、reset、checkout，也没有回退这些变化。首次暂存内容清单仅代表任务开始时快照。
