---
title: 用 Ansible 管理 VPS：告别手动配置服务器
date: 2026-02-12 00:00
excerpt: 用 Ansible 把 VPS 的系统初始化和 Docker 服务部署全部自动化，一条命令从裸机到所有服务就绪
tags:
  - Ansible
  - Docker
  - VPS
---

# 用 Ansible 管理 VPS：告别手动配置服务器

前段时间我的 Cloudcone VPS 突然崩了，上面跑着好几个服务，结果只能重新买一台，然后手动一步步把环境和服务全部重新搭建。升级系统、装 Docker、配 fail2ban、拉各种容器……整个过程既繁琐又容易遗漏。这次经历让我意识到，如果服务器随时可能挂掉，那我需要一种能快速重建整个环境的方式——最好是一条命令就能搞定。

于是我用 Ansible 把 VPS 的配置和服务部署全部自动化了。这篇文章记录一下整个方案，项目结构很简单，但足够覆盖个人服务器的日常需求。

## 技术选型

- **Ansible**：配置管理工具，通过 SSH 连接远程机器执行任务，不需要在目标机器上装 agent
- **uv**：Python 包管理器。Ansible 本身是 Python 写的，我不想用 `brew install ansible` 或 `pip install ansible` 污染本机的软件环境，所以用 uv 创建项目级的虚拟环境来管理依赖
- **Docker Compose**：所有应用服务都容器化部署

配置管理工具我在 Ansible 和 Salt 之间纠结了一下，之前看到 Cloudflare 的博客提到他们用的是 Salt。不过 Salt 需要在目标机器上装 minion agent，架构更重一些，适合管理大规模集群。我只有一台 VPS，Ansible 通过 SSH 直接连接就够了，agentless 的方式更轻量，也不用维护额外的组件。

## 项目结构

```
my-servers/
├── ansible.cfg          # Ansible 配置（SSH 连接复用、pipeline 等）
├── inventory.yml        # 主机清单
├── setup.yml            # 主 playbook：初始化 + 部署所有服务
├── xxx.yml              # 各服务的 Docker Compose 文件
├── pyproject.toml       # Python 项目配置（声明 ansible 依赖）
└── uv.lock              # 依赖锁定文件
```

结构很扁平：根目录放各个服务的 Docker Compose 文件，`setup.yml` 是唯一的 playbook，负责初始化系统和部署所有服务。

## 环境搭建

用 `uv` 管理 Python 环境和 Ansible 依赖：

```toml
# pyproject.toml
[project]
name = "my-servers"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "ansible>=13.3.0",
]
```

```bash
# 安装依赖
uv sync

# 之后所有 ansible 命令都通过 uv run 执行
uv run ansible-playbook setup.yml
```

这样做的好处是不污染全局 Python 环境，换台电脑 clone 下来 `uv sync` 就能用。

## 主机配置

`inventory.yml` 定义了要管理的机器：

```yaml
all:
  hosts:
    cloudcone:
      ansible_host: 72.18.xx.xx
      ansible_user: root
      ansible_port: 22
      ansible_ssh_private_key_file: ~/.ssh/cloudcone
```

用 SSH 密钥认证连接 VPS。如果还没有密钥对，先在本机生成：

```bash
ssh-keygen -t ed25519 -f ~/.ssh/cloudcone -C "cloudcone"
```

然后把公钥传到 VPS 上：

```bash
ssh-copy-id -i ~/.ssh/cloudcone.pub root@72.18.xx.xx
```

之后就可以免密登录了。如果以后加机器，在 `inventory.yml` 里加一组 host 就行。

`ansible.cfg` 做了一些 SSH 优化：

```ini
[ssh_connection]
# 复用 SSH 连接，避免每个 task 重新握手
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
# 用管道传输模块，减少一次 SFTP 往返
pipelining = true
```

这两个配置能显著加快 playbook 的执行速度，尤其是 task 数量多的时候。

## Playbook 详解

`setup.yml` 是整个项目的核心，分为两大部分：系统初始化和服务部署。

### 系统初始化

前置条件是目标服务器需要先手动升级到 Debian 13（Trixie）。Cloudcone 的面板目前没有提供 Debian 13 的系统镜像，所以我用了 [reinstall](https://github.com/bin456789/reinstall) 这个脚本来重装系统，它支持在任意 Linux 发行版上一键重装到指定版本的 Debian，非常方便。

系统准备好之后，playbook 会自动完成：

**1. 安装 Python3**

Ansible 依赖目标机器上的 Python，但一些极简系统镜像可能没有预装。所以用 `raw` 模块先装上：

```yaml
pre_tasks:
  - name: 安装 Python3（Ansible 依赖）
    ansible.builtin.raw: apt-get update && apt-get install -y python3
    changed_when: false
```

`raw` 模块不依赖 Python，直接在远程 shell 执行命令，专门用来解决这种鸡生蛋的问题。

**2. 系统更新 + 基础软件包**

```yaml
- name: 更新 apt 缓存并升级所有包
  ansible.builtin.apt:
    update_cache: true
    upgrade: dist

- name: 安装基础包
  ansible.builtin.apt:
    name:
      - fail2ban
      - ca-certificates
      - curl
      - gnupg
    state: present
```

**3. 配置 fail2ban 防 SSH 爆破**

```yaml
- name: 配置 fail2ban SSH 防爆破
  ansible.builtin.copy:
    dest: /etc/fail2ban/jail.local
    content: |
      [sshd]
      enabled = true
      port = ssh
      backend = systemd
      maxretry = 3
      findtime = 600
      bantime = 3600
    owner: root
    group: root
    mode: "0644"
  notify: 重启 fail2ban
```

3 次失败就封禁 1 小时，算是最基本的安全措施。

**4. 安装 Docker**

遵循 Docker 官方文档的安装方式，Debian 13 已经废弃了 `apt_key`，所以直接把 GPG 密钥下载到 keyrings 目录：

```yaml
- name: 添加 Docker 官方 GPG 密钥
  ansible.builtin.get_url:
    url: https://download.docker.com/linux/debian/gpg
    dest: /etc/apt/keyrings/docker.asc
    mode: "0644"

- name: 添加 Docker apt 仓库
  ansible.builtin.apt_repository:
    repo: >-
      deb [signed-by=/etc/apt/keyrings/docker.asc]
      https://download.docker.com/linux/debian
      {{ ansible_facts['distribution_release'] }} stable
    state: present
    filename: docker
```

用 `ansible_facts['distribution_release']` 自动获取发行版代号，不用硬编码。

### 服务部署

每个服务的部署都遵循同样的三步模式：

```yaml
# 1. 创建部署目录
- name: 创建 XXX 部署目录
  ansible.builtin.file:
    path: /opt/xxx
    state: directory
    mode: "0755"

# 2. 复制 Docker Compose 文件
- name: 复制 Docker Compose 文件到远程
  ansible.builtin.copy:
    src: xxx.yml
    dest: /opt/xxx/docker-compose.yml
    mode: "0644"

# 3. 启动服务
- name: 启动 XXX 服务
  community.docker.docker_compose_v2:
    project_src: /opt/xxx
    state: present
    pull: always
```

`pull: always` 确保每次执行都会拉取最新镜像。`community.docker.docker_compose_v2` 是 Ansible 的 Docker Compose 模块，比直接 `shell: docker compose up -d` 更好，因为它是幂等的——多次执行不会产生副作用。

### 目前部署的服务

| 服务 | 用途 | 端口 |
|---|---|---|
| New-API | LLM API 网关，聚合多家大模型 API | 3000 |
| Claude2API | Claude 代理 | 8080 |
| RSSHub | RSS 订阅源生成 | 1200 |

## 日常使用

```bash
# 从零初始化一台新 VPS（执行全部任务）
uv run ansible-playbook setup.yml

# 只部署某个服务（跳到指定任务开始执行）
uv run ansible-playbook setup.yml --start-at-task="创建 RSSHub 部署目录"

# 检查语法，不实际执行
uv run ansible-playbook setup.yml --check

# 测试连通性
uv run ansible all -m ping
```

`--start-at-task` 在只改了某个服务的 Compose 文件时特别有用，不需要跑完整个 playbook。

## 添加新服务

添加一个新服务只需要两步：

1. 在项目根目录创建 `<service>.yml`（Docker Compose 文件）
2. 在 `setup.yml` 里加三个 task（创建目录、复制文件、启动服务）

模式是固定的，复制粘贴改个名字就行。

## 一条命令走天下

日常使用下来，最爽的一点是所有操作都收敛到了同一条命令：

```bash
uv run ansible-playbook setup.yml
```

不管是什么场景，都是跑这一条：

- **部署到新 VPS**：买了台新机器，配好 SSH 密钥，改一下 `inventory.yml` 里的 IP，跑一遍，从裸机到所有服务就绪
- **加新服务**：写好 Docker Compose 文件，在 `setup.yml` 里加三个 task，跑一遍
- **升级现有服务**：镜像用的是 `latest` tag，直接跑一遍，`pull: always` 会自动拉取最新镜像并重建有变更的容器，什么都不用改

这得益于 Ansible 的幂等性——已经完成的步骤会自动跳过，只执行有变更的部分。所以不用担心重复执行会出问题，也不需要记住「上次跑到哪了」。心智负担几乎为零。

## 总结

这个项目的核心思路很简单：**把服务器配置当代码管理**。好处是：

- **可复现**：VPS 挂了一条命令就能在新机器上恢复所有服务
- **可追溯**：所有配置变更都有 git 记录
- **可维护**：改个配置提交推送，跑一下 playbook 就生效

对于只有一两台 VPS 的个人用户来说，不需要 Kubernetes 那套复杂的东西，Ansible + Docker Compose 就足够了。
