---
title: 一次配置，处处运行：在 Dev Containers 中开发
date: 2025-04-09 16:52
excerpt: 如何使用 Dev Containers 作为环境进行开发，享受统一的 Linux 环境
category: 工具
---
# 背景
本来我一直是在本地的 Windows 或者 macOS 上进行开发的，也没出过什么问题

但是在某次对一个前端项目升级依赖后，部署到 cloudflare pages 上的预览功能突然不能用了，报错显示

> ⚡️ @cloudflare/next-on-pages CLI v.1.13.7
>
> ⚡️ Warning: It seems like you're on a Windows system, the Vercel CLI (run by @cloudflare/next-on-pages
> ⚡️ to build your application) seems not to work reliably on Windows so if you experience issues during
> ⚡️ the build process please try switching to a different operating system or running
> ⚡️ @cloudflare/next-on-pages under the Windows Subsystem for Linux

直接提示我没法在 Windows 上用，也是离大谱了，按理说这个时候最好的选择是用 wsl，但是之前折腾过一次，网络配置有点麻烦，索性要折腾，就一步到位吧，所以还是选择了 Dev Containers 这种方法，比 wsl 更有普适性

# 开发容器是什么？
开发容器首先是一个容器，其次它可以像物理机一样，作为代码运行的环境。

想象一下，你可以为你的项目量身定做一个“集装箱”，里面预装了所有必需的工具、依赖库、运行时环境，甚至特定版本的操作系统。这个“集装箱”就是开发容器。

通过像 VS Code 这样的编辑器配合开发容器扩展，你可以做到：

1.  直接在容器内打开和编辑你的项目代码：你的代码文件可以从本地挂载到容器中，或者直接克隆/复制进去。
2.  享受完整的编辑器功能：代码智能提示、自动补全、代码跳转、断点调试等 VS Code 功能，以及其他第三方拓展支持的功能，都可以在容器内无缝运行。
3.  环境定义与代码同行：项目中的一个 `devcontainer.json` 文件负责定义这个容器环境的一切——需要什么工具、哪个版本的运行时、需要自动安装哪些 VS Code 扩展等等。这个配置文件随着你的代码库一起版本控制。
4.  隔离与一致性：每个项目都可以拥有自己独立的、隔离的开发环境，确保团队成员之间、以及开发/测试/生产环境之间的高度一致性，彻底告别“环境不一致”的烦恼。
5.  快速切换与启动：切换不同项目就像连接到不同的容器一样简单，新成员加入项目也能迅速获得一个“开箱即用”的开发环境。

下图是开发容器和宿主机的交互示意：

![](https://code.visualstudio.com/assets/docs/devcontainers/containers/architecture-containers.png)

# 安装
一般来说还是推荐使用本地的容器，所以就先需要安装 Docker Desktop，这里不赘述了，不是本文关键，参考[官网](https://docs.docker.com/get-started/get-docker/)即可

在 Windows 上，Docker Desktop 需要 wsl 作为后端，所以其实相当于也还是用了 wsl，不过又在 wsl 上包装了一层，更方便使用了

# 配置
## git 行尾
因为容器中是 Linux 环境，所以使用 git 的时候还需要设置一下行尾，可以参考：https://code.visualstudio.com/docs/remote/troubleshooting#_resolving-git-line-ending-issues-in-wsl-resulting-in-many-modified-files

简单来说就是，在 git 仓库的根目录下再新建一个 `.gitattributes` 文件，强制文件使用 Linux 的 LF 行尾，某些 Windows 专有文件除外：

```
* text=auto eol=lf
*.{cmd,[cC][mM][dD]} text eol=crlf
*.{bat,[bB][aA][tT]} text eol=crlf
```
## git config
开发容器会无脑把本地的一些文件复制到容器里，比如 `.gitconfig`，这一点还不好在 `.devcontainer.json` 里配置，这对于网络环境比较复杂的中国开发者来说，就会带来一些额外的麻烦

比如，在看完官网文档，进行[第一个实践](https://code.visualstudio.com/docs/devcontainers/containers#_quick-start-try-a-development-container)的时候，很可能会遇到无法 git clone 的报错，就是这个问题引起的

这个时候可以把本地的 `.gitconfig` 中关于代理的部分注释掉，按理说这个地方应该编辑一下 `.devcontainer.json` 把容器网络配置好，但是有简单的方法用，我就不搞复杂的了

或者还有一种方法，在 vscode 设置中，`dev.containers.copyGitConfig` 设置为 `false`，也就是图形化设置里的打钩取消

然后就没有全局的 `.gitconfig` 了，但是根据默认设置，git credential 还是会被复制过去，不影响权限，只是需要手动设置一个用户名和邮箱

我也试了一下[有些人](https://github.com/microsoft/vscode-remote-release/issues/4603)提到的更改 `.devcontainer.json` 中的 `postCreateCommand`，但是似乎不起作用

## ssh 设置
### 没用的小方法
有的时候如果使用 ssh 而不是 http/https 连接 git，就需要一些额外的配置

从这一步开始就有一点不一样了，为了启动 ssh-agent，在 macOS 上使用 `eval "$(ssh-agent -s)"`

在 Windows 上，假设你之前已经正常安装过 ssh 了，现在在“服务”中，找到 `OpenSSH Authentication Agent`，然后启动这个服务

对于这两个操作系统来说，下面的命令是一样的，用 `ssh-add -l` 验证 ssh-agent 是否有效

如果运行正常，但没有加载密钥，会看到 `The agent has no identities.`

然后加载私钥到 ssh-agent，比如：`ssh-add ~/.ssh/id_xxx`

顺便说一下，`.ssh/` 下可能会有两个文件，`id_xxx` 是私钥，`id_xxx.pub` 是公钥

加载完成后，再用 `ssh-add -l` 验证，就能看到刚才添加的私钥信息

如果这个时候又因为代理报错了，可以先把代理管理，把私钥加上，再把代理开回来，不影响后续使用

现在已经添加好了，想要验证一下 ssh 是用了 ssh-agent 还是直接用了本地文件，可以用 `ssh -v -T user@hostname` 测试一下

如果正常使用了 ssh-agent，就会看到类似的信息 `debug1: Server accepts key: <path> <algorithm> <hash> explicit agent`

如果直接用了本地文件没有用代理，信息就是 `debug1: Server accepts key: <path> <algorithm> <hash> explicit`

虽然理论上来说，似乎按照官方文档，这一步之后就已经可以用了，但是我试了试不行

### 直接挂载 ssh 目录
所以我也不搞那么复杂了，直接把本地的 `.ssh` 目录挂载过去，简单粗暴

在 `devcontainer.json` 中添加：

```json
"remoteUser":"root",
"mounts":[
    "source=${localEnv:HOME}${localEnv:USERPROFILE}/.ssh,target=/root/.ssh,type=bind,consistency=cached"
]
```

这里注意挂载的目标路径要和你的远程用户相符

这里可能会报一个错误 `Bad owner or permissions on /root/.ssh/config`，这个似乎跟所有者和权限有关，因为是自己开发，我就用比较简单粗暴的方法修复了：

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/*
```

之后还可以把上面的命令添加到 `postCreateCommand` 里

## 拓展
dev container 创建的时候，会自带一些拓展，这一点可以在 `dev.containers.defaultExtensionsIfInstalledLocally` 中修改，这是一个全局的设置

我这里默认的内容有 `"GitHub.copilot"`

如果在某个开发容器里，还想要把其他本地拓展安装进去，可以在本地的拓展上右键，选择 `添加到 devcontainer.json`，然后 rebuild 即可

当然也可以手动修改拓展配置，下面是一个例子：
```json
"customizations": {
		"vscode": {
			"extensions": [
				"streetsidesoftware.code-spell-checker",
				"GitHub.copilot",
				"mhutchie.git-graph"
			]
		}
	},
```

## 设置
有时候在容器里，需要的配置还和外面的配置不太一样，就需要自定义一下

比如在外面设置了 `http.proxy`，但是容器里不需要这个代理，保持这个设置还会让 github copilot 无法使用

如果需要改配置，像这样修改：
```json
"customizations": {
		"vscode": {
			"settings": {
				"editor.fontSize": 12
			}
		}
	},
```
这里只能修改可以在 workspace settings 中修改的设置，根据[官方文档](https://code.visualstudio.com/docs/getstarted/settings#_workspace-settings:~:text=Not%20all%20user%20settings%20are%20available%20as%20workspace%20settings.%20For%20example%2C%20application%2Dwide%20settings%20related%20to%20updates%20and%20security%20can%20not%20be%20overridden%20by%20Workspace%20settings.)，对于部分 user settings，是无法修改的

很不巧，`http.proxy` 就是这种设置，没法在 `customizations.vscode.settings` 里设置，于是我自己把 user settings 里的设置改掉了

**提了 issue，这个功能不知道会不会改，后续再看看吧**

## 基础环境
上面的所有配置基本上是不分项目和语言的，下面就和语言比较相关了，需要配置和语言相关的环境
### 从镜像构建
比较简单的做法是直接设置 `image` 属性，这样就有一个基础的环境了，比如 `"image": "mcr.microsoft.com/devcontainers/javascript-node:1-18-bullseye"`

或者 `"image": "node:latest"` 

### 从 Dockerfile 构建
这种方法用 Dockerfile 提供基础环境，比用 `image` 自由度稍高一点

我个人是比较喜欢 Dockerfile，比 `image` 加 `postCreateCommand` 好一点

不过对于有的需要在项目目录下执行的命令，还是用 `postCreateCommand` 方便一点，比如 `pnpm install`，一些可以全局执行的命令就无所谓了

使用 Dockerfile，就不需要 `image` 了，要设置 `build.dockerfile` 为 `Dockerfile` 对于 `devcontainer.json` 的相对地址

一般来说，`.devcontainer` 文件夹下会有 `devcontainer.json` 文件和 `Dockerfile` 文件

然后 `devcontainer.json` 文件中的配置是：

```json
"build": {
		"dockerfile": "Dockerfile"
	},
```

### 从模板构建
另一个比较简单的做法是使用[开发容器模板](https://containers.dev/implementors/templates/)

这部分的文档写得很差，我只能简单说一下似乎正确的使用方式

模板都是官方和社区提供的，这种方式是自己写好模板后推送到一个中央仓库，然后用户从中央仓库拉取，所以不太适合小范围分享模板

使用方法是用 vscode, Ctrl + Shift + P 打开命令面板，然后选择 dev containers: add dev container configuration files

然后就可以选择想使用的模板了，选择完之后会生成相应的配置文件




## 源代码存储的位置
使用开发容器，实际上有两种方法：
- 把文件全部放在容器中（dev containers: clone repository in container volume）
- 把文件放在本地（dev containers: open folder in container）

比较推荐的是第一种做法，上面很多繁琐的配置也是基于第一种方法做的，如果把本地放在本地，有的配置就可以比较简单

但是把文件放在本地，而且本地操作系统是 Windows 或 macOS，跨文件系统就会有比较严重的性能问题

如果非要这么做记得看一下注意点：https://code.visualstudio.com/remote/advancedcontainers/improve-performance

## postCreateCommand
前面说了很多 `postCreateCommand`，是用于在项目目录下执行命令，可以接受字符串、对象或者数组，但是我的体验是，如果命令很多，用数组把命令一条一条塞进去，并不好用，不知道为什么会报错

如果只有很短的一条或者几条就算了，直接写成字符串，比如 `"postCreateCommand": "pnpm install"`

如果命令比较多的话，建议单独创建一个脚本 `install.sh`，在里面写好命令，然后 `"postCreateCommand": "chmod +x install.sh && ./install.sh"`

## 其他
如果修改配置后，重新生成容器还不行，可以试试把 Docker Desktop 里的相关 containers 和 volumes 删了，这样可以确保新的容器完全按照新配置生成

如果发现开发容器内自动使用了本机的代理，这个代理又不在容器中，导致网络访问异常，可以在 vscode 的设置中，对于开发容器的设置，找到 `http.useLocalProxyConfiguration` 这一项，把✅去掉

# 最终效果
这样，针对 git 仓库的开发容器就设置好了，你可以在任何一个包含 docker 和 vscode 的设备上，无需任何其他环境配置，直接进行开发，非常方便

甚至在 GitHub 的网页端，也可以直接利用 Codespaces 读取开发容器配置，启动一个云端环境进行开发