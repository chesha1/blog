---
title: 在同一台设备上，使用多个 GitHub 账号
date: 2024-09-09 16:03
excerpt: 使用 SSH 密钥进行连接，并且在仓库级别使用独立的配置
category: 工具
tags: 
  - GitHub
---
# 背景
有时候，因为工作或者别的需要，会使用多个 GitHub 账号区分身份，但是同一台电脑上，全局设置只对一个账号生效

为了使用多个身份，具体的操作，简单来说就是先设置使用 SSH 连接 GitHub，然后在仓库层面修改设置，使用这个 SSH 连接，而不使用全局的 `.gitconfig`

仅为自用记录一下，如有错误，请多包涵

# 具体操作
## 生成 SSH 密钥
首先检查一下本地是否有 OpenSSH，并看一下版本：
```shell
ssh -V
```

如果有的话，到 `~/.ssh` 目录下生成一对 SSH 密钥：
```shell
ssh-keygen -t ed25519 -C "your_email@example.com" -f "id_github_new"
```
这里推荐使用 ed25519，比 rsa 更安全，而且密钥更短

然后会出现两个文件：`id_github_new.pub` 和 `id_github_new`

## 在 GitHub 上设置密钥
到 GitHub 网页端，进入 Settings - SSH and GPG keys

在 SSH keys 的部分，点击绿色的按钮，New SSH key

Key type 就用默认的 Authentication Key

Key 的内容填写刚才生成的 `id_github_new.pub` 中的内容

## 设置本地的 SSH 连接
到本地的 `~/.ssh/config` 中设置一下 SSH 连接，如果这个文件不存在，要创建一下

一个示例如下：

```
Host github-new
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_github_new
```

`Host` 后面的内容是自定义的名称，可以使用任何不冲突的名字，它将作为 GitHub 的别名，方便在命令中使用

`HostName` 和 `User` 的内容不能改

`IdentityFile` 的内容就填刚才用 `ssh-keygen` 生成出来的文件的地址

## 测试连接
用 `ssh -T <User>@<Host>`测试一下是否可以连接

在本次的例子中，就是：

```shell
ssh -T git@github-new
```

第一次连接的时候，因为这个地址不在 `known_hosts` 里，会显示 `Are you sure you want to continue connecting (yes/no/[fingerprint])?`

这里记得明确输入 `yes`，默认敲一个回车是不行的

然后就会有成功的提示：

```
Hi <userName>! You've successfully authenticated, but GitHub does not provide shell access.
```

关于使用 SSH 连接 GitHub，官网有[更详细的说明](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh)，可以参考一下

## 使用新身份操作 git
git 有很多配置，仓库底下的 `.git/config` 的优先级会高于全局的

所以，在用任意账号，把一个仓库 `git clone` 下来之后，更改一下这个仓库的设置

在仓库的目录下：
```shell
git remote set-url origin git@<Host>:<github_user_name>/<repo_name>.git
git config user.name <user_name>
git config user.email <user_email>
```

记得把 <> 中的内容替换成真实的值，在本次的例子中，比如：
```shell
git remote set-url origin git@github-new:your_github_user_name/test-repo.git
git config user.name your_github_user_name
git config user.email your_email@example.com
```

这样设置好之后，对仓库进行的操作，用的就是新用户的身份了

然后可以用 `git ls-remote origin` 测试一下设置是否成功，尝试连接到 `origin` 远程仓库，并列出所有远程引用

如果成功，你会看到类似以下输出：
```shell
<commit-hash>  refs/heads/main
<commit-hash>  refs/heads/other-branch
```

再用 `git push --dry-run` 需要验证是否有推送权限，这会模拟推送过程而不会实际更改远程仓库