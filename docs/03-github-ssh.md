# 1.3 GitHub 联动与编辑器初步调优
>💡 本章目标：建立本地电脑与 GitHub 云端的信任链路（SSH），并对 VS Code 进行基础调优，确保开发环境既符合中文直觉，又具备稳定性。这一阶段的操作，同样在新电脑上只需要做一次。

## 一、 GitHub 联动：配置 SSH 密钥

### 1. SSH 密钥是什么、为什么要用？

SSH 密钥是一对配对的文件：

- **公钥**（public key）：可以公开分享，用于验证身份
- **私钥**（private key）：**必须保密**，存放在本地，用于证明身份

**工作原理**（不严格但够用的比喻）： 公钥像一把**挂在 GitHub 上的锁**，私钥是**留在你电脑里的钥匙**。每次推送代码时，Git 会自动用本地私钥去开 GitHub 上的锁，开得开就放行，开不开就拒绝。

>💡为什么不用密码？
>- **免密安全**：配置后，每次推送代码无需输入账号密码，且安全性远高于普通密码。
>- **身份唯一性**：确保 GitHub 知道这行代码确实是你本人提交的，而不是冒名顶替。

### 2. SSH 密钥生成与配置步骤

#### 第 1 步：先检查本机是否已有 SSH 密钥
>⚠️ GitHub 官方建议：生成新密钥之前先检查本机有没有现成的，避免重复生成覆盖掉旧密钥。

在 PowerShell 中输入：

```powershell
ls -al ~/.ssh
```
如果看到 `id_rsa` 和 `id_rsa.pub` 这对文件，说明你已经有 SSH 密钥了，可以直接跳到第 3 步。

如果文件夹是空的或提示 `No such file or directory` → 按第 2 步生成新密钥。

#### 第 2 步：生成新密钥

在 PowerShell 中输入：

```powershell
# 请将引号内的内容替换为你自己的 GitHub 信息
ssh-keygen -t ed25519 -C "你的GitHub邮箱@example.com"
```

连续按三次回车，保持默认路径，不设密码。

#### 第 3 步：获取公钥
在 PowerShell 中输入：

```powershell
cat ~/.ssh/id_ed25519.pub
```

复制输出的完整内容（以 `ssh-ed25519` 开头的一整行）。

>⚠️ 复制的是 `.pub` 公钥文件内容，不是无后缀的私钥！如果误把私钥贴到 GitHub，等于把家门钥匙挂到了网上。

#### 第 4 步：将公钥添加到 GitHub
1. 登录 GitHub。
2. 点击右上角的头像，选择 **Settings**。
3. 在左侧菜单中选择 **SSH and GPG keys**。
4. 点击 **New SSH key**。
5. 在 **Title** 字段中输入一个描述性的名称（如 `my-laptop`）。
6. 将复制的公钥粘贴到 **Key** 字段中。
7. 点击 **Add SSH key**。

#### 第 5 步：测试连接

在 PowerShell 中输入：

```powershell
ssh -T git@github.com
```

>⚠️ 首次连接必踩的坑： 执行后会出现以下提示：
>```powershell
>The authenticity of host 'github.com' can't be established.
>Are you sure you want to continue connecting (yes/no/[fingerprint])?
>```
>**必须手动输入 `yes` 并回车**，不能直接按回车，否则连接会被拒绝。 这个提示只会出现一次，之后不再询问。

看到 `Hi 用户名! You've successfully authenticated` 即成功。

---

## 二、 全局身份署名

为了让你的每一次代码提交都有迹可循，必须告诉 Git “你是谁”：

```powershell
# 请将引号内的内容替换为你自己的 GitHub 信息
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱@example.com"
```

- 这是一次性配置，将对你电脑上所有的 Git 项目生效
- 以后每次提交代码时，Git 都会自动带上这个身份信息，GitHub 上也会显示你的用户名和头像。

--- 
## 三、 VS Code 初始调优

在正式写代码前，我们要先对 VS Code 进行一些基础调优，有利于提升开发体验。

### 1. 安装插件
- 打开 VS Code，点击左侧的扩展图标（四个方块组成的图标）或按 `Ctrl+Shift+X` 进入插件市场。
- 搜索并安装以下插件：

| 插件名 | 用途 | 为什么必须装？ |
| :--- | :--- | :--- |
| **Python** (Microsoft) | Python 基础语言支持 | 环境的“地基”，提供运行和调试功能。 |
| **Pylance** | 代码智能提示与静态检查 | **拦截红线的第一道防线**，实现 Basic 级别代码检查。 |
| **Ruff** (Astral Software) | **极速**格式化与代码纠错 | 代替传统工具，实现“保存即对齐”，自动清理无用 import。 |
| **GitLens** | 源代码管理与历史回溯 | 视觉化查看每一行代码的“前世今生”，重构时的救命稻草。 |
| **GitHub Copilot** | AI 辅助编程  | 自动补全逻辑、生成单元测试，极大提高生产力。 |
| **GitHub Copilot Chat** | AI 架构讨论与纠错 | 直接在编辑器内与 AI 讨论重构方案，解决环境报错。 |
| **Chinese (Simplified)** | 汉化界面 | （可选）降低新手上手门槛。 |
| **indent-rainbow** | 缩进颜色区分 | 物理视觉对齐，防止 Python 因为缩进导致的低级错误。 |
| **Material Icon Theme**| 文件图标美化 | 快速通过图标分辨 `.py`、`.bat`、`.toml` 等不同文件类型。 |
| **Code Runner (formulahendry)**| 一键运行任意代码片段 | 提供右上角的“播放键”，无需每次手动敲 `uv run xxx.py`，可测试局部逻辑。 |

### 2. 把默认终端切换为 Git Bash

VS Code 在 Windows 上的默认终端是 **PowerShell**，需要手动切换为 Git Bash：

`Ctrl+Shift+P` → 输入 `Terminal: Select Default Profile` → 选 `Git Bash`

> 切换后，新打开的终端会默认是 Git Bash，避免 PowerShell 的兼容性问题（很多教程命令都是按 Bash 语法写的）。

### 3. 开启自动保存


`文件` → `自动保存`，打上勾。


### 4.  `settings.json` 配置

在 VS Code 的世界里，如果说插件是你的工具，那么 `settings.json` 就是这个工坊的“灵魂”与“总控制台”。

简单来说，它是一个以 `.json` 格式存储的纯文本文件，记录了你对编辑器所有的个性化要求——从字体大小这种视觉偏好，到“保存即自动排版”这种高级自动化逻辑。

`Ctrl+Shift+P` → 输入 `Open User Settings JSON`，添加：

#### 1. 它能帮你做什么？

- 通过配置 `settings.json`，你可以强制编辑器执行以下“工程化”行为：

- 全自动管家：开启 `editor.formatOnSave` 后，你乱敲的代码会在按下保存键的瞬间，被自动对齐、缩进、并梳理好逻辑顺序。

- 物理防灾：配置 `files.autoSave`（自动保存）和 `files.encoding`（强制 UTF-8），能从底层避免代码丢失或中文乱码的低级错误。

精准指派：你可以为不同的语言指定不同的“蓝领工人”。比如在 `[python]` 模块下，指定使用 `Ruff` 作为默认的格式化工具，并让它在保存时自动删除没用的代码导入。

#### 2. 为什么它是“代码”形式，而不是菜单？

虽然 VS Code 提供了图形化的设置界面（点点鼠标的那种），但专业开发者更偏爱直接编辑 `settings.json`：

1. 极速配置：当你拿到一台新电脑，只需把这一段 JSON 代码粘贴进去，几秒钟就能找回你最顺手的开发环境。

2. 绝对精准：图形界面有时会隐藏深度选项，而配置文件允许你进行最细颗粒度的参数调整。

3. 版本化管理：你可以像管理代码一样备份它，确保你的开发习惯是可复现、可迁移的。

#### 3. 如何找到它？
它被隐藏在 VS Code 的万能入口中：

- 按下快捷键 `Ctrl + Shift + P` 呼出命令面板。

- 输入 `Open User Settings JSON` 并点击。

>⚠️提示：在编辑这个文件时，哪怕漏掉一个逗号 `,` 或引号 `"`，VS Code 都会通过红线警告你。因此，**养成在修改前先备份一份原始配置的习惯**，以防不小心把编辑器变成了“砖头”。

下面是一份`settings.json`模板：

```json
{
  // ==========================================
  // 1. 核心编辑器与基础交互 
  // ==========================================
  "editor.fontSize": 14,                            // 代码字号，按需调整
  "editor.tabSize": 4,                              // Python 缩进：必须是 4 个空格，严禁混用 Tab 和空格
  "editor.wordWrap": "on",                          // 自动换行，写 Markdown 手册和看长注释时不用横向拉滚动条
  "files.autoSave": "afterDelay",                   // 开启自动保存防呆机制，防断电、防意外关闭
  "files.autoSaveDelay": 1000,                      // 停止敲键盘 1 秒后触发自动保存（配合 Ruff 能实现“停手即排版”）
  "workbench.colorTheme": "One Dark Pro",           // 护眼暗色主题，长时间盯屏幕必备
  "workbench.iconTheme": "material-icon-theme",     // 替换默认文件图标，可视化区分 .py、.toml、.bat 等不同文件类型
  "workbench.secondarySideBar.defaultVisibility": "visible", // 默认显示辅助侧边栏，方便多线操作
  "chat.viewSessions.orientation": "stacked",       // 将聊天视图折叠堆叠，节省屏幕空间

  // ==========================================
  // 2. Python 引擎与工程化 
  // ==========================================
  "python.analysis.typeCheckingMode": "basic",      // 开启 Pylance 基础静态检查，拦截逻辑漏洞
  "python.terminal.activateEnvironment": true,      // 每次打开终端自动激活 .venv，省去手动激活
  
  // 针对 Python 文件的自动化规范控制
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff", // 抛弃自带工具，使用极速的 Ruff 作为默认格式化器
    "editor.formatOnSave": true,                     // 开启“保存即对齐”
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",                   // 保存时自动修复低级错误（如删掉没用的变量）
      "source.organizeImports": "explicit"           // 保存时自动将 import 的库按字母顺序排好，告别杂乱
    }
  },

  // ==========================================
  // 3. Git 与代码时光机 
  // ==========================================
  "git.autofetch": true,                            // 自动拉取云端最新状态，防代码冲突
  "git.confirmSync": false,                         // 点击同步时不再反复弹窗确认，提升效率
  "git.openRepositoryInParentFolders": "never",     // 专注当前项目，不跨级扫描父文件夹的 Git 仓库，防止卡顿

  // GitLens 增强功能
  "gitlens.codeLens.enabled": true,                 // 在代码函数上方，悬浮显示是谁写的、什么时候改的
  "gitlens.currentLine.enabled": true,              // 在当前鼠标光标所在的行末尾，显示该行的修改历史

  // ==========================================
  // 4. AI 助手 
  // ==========================================
  // GitHub Copilot 全局控制
  "github.copilot.nextEditSuggestions.enabled": true, // 开启预测性建议，AI 会猜你下一步想改哪里
  "github.copilot.enable": {
    "*": true,                                      // 默认全语言开启 Copilot
    "plaintext": false,                             // 普通纯文本文件不启用，防干扰
    "markdown": true,                               // 写说明文档时开启，方便写手册
    "scminput": false                               // 提交代码的输入框不启用
  },
  
  // GitLens 与 AI 的深度绑定
  "gitlens.ai.model": "vscode",                     // 告诉 GitLens 使用 VS Code 内部的 AI 通道
  "gitlens.ai.vscode.model": "copilot:gpt-4.1", // 指定模型，可选项包括：
                                              // - "copilot:gpt-4.1"（推荐，最新版本，理解力更强）
                                              // - "copilot:gpt-3.5"（旧版本，偶尔理解错误但响应更快）

  // 其他 AI 插件配置
  "claudeCode.preferredLocation": "panel",          // 将 Claude Code 面板固定在下方控制台区域
  "chat.mcp.gallery.enabled": true,                 // 开启 AI 对话的模型上下文协议画廊支持

  // ==========================================
  // 5. 终端与一键运行集成 
  // ==========================================
  "code-runner.runInTerminal": true,                // 用 Code Runner 跑代码时，强制在终端输出，支持交互输入
  "code-runner.saveFileBeforeRun": true,            // 运行前自动保存，防止跑了半天还是旧代码

  // 将 Git Bash 设置为 Windows 下的唯一指定终端
  "terminal.integrated.defaultProfile.windows": "Git Bash", 
  "terminal.integrated.profiles.windows": {
    "Git Bash": {
      "path": "D:\\Program Files\\Git\\bin\\bash.exe", // 确保此路径与你的 Git 实际安装位置一致
      "args": ["--login", "-i"]
    },
    "PowerShell": {
      "source": "PowerShell",
      "icon": "terminal-powershell"
    },
    "Command Prompt": {
      "path": [
        "${env:windir}\\Sysnative\\cmd.exe",
        "${env:windir}\\System32\\cmd.exe"
      ],
      "args": [],
      "icon": "terminal-cmd"
    }
  }
}
```
>💡 **配置说明**：
>- 以上配置是基于个人使用习惯和效率优化的建议，**不必照搬**，可以根据自己的喜好进行调整。
>- 重点是理解每一项配置背后的目的，确保你的编辑器环境既符合中文用户的直觉，又能最大程度地提升开发效率和代码质量。
>- 部分配置可能会与某些插件产生冲突，安装插件后如果发现编辑器行为异常，请先检查是否有配置项需要调整或注释掉。
>- 某些配置可能需要特定插件才能生效（如 `editor.defaultFormatter` 需要安装对应的格式化插件），请确保相关插件已正确安装并启用。

配置完成后，**务必重启 VS Code**，让所有设置生效。

### 5. 跨平台编码与行结尾符
在 Windows 上开发时，如果不注意编码，发给 Linux/Mac 系统的同事可能会出现乱码。

- 全局 UTF-8：在 VS Code 右下角状态栏，确保显示的是 UTF-8。如果不是，请点击它并选择“通过编码重新保存”。

- 行结尾符 (LF)：Windows 默认使用 CRLF，但建议统一使用 LF，以保持跨平台的一致性。

### 6. 常用快捷键
| 快捷键        | 功能                 | 场景 |
| :---  | :--- | :--- | 
| `Ctrl + `` `       | 打开 / 关闭终端        |快速切换写代码与输命令的状态。 |
| `Ctrl + Shift + P` | 命令面板（万能入口）       |找不到功能时，先按这个搜一下。 |
| `Ctrl + P`         | 快速打开文件           |当你有几十个文件时，搜索比鼠标点更快。 |
| `Ctrl + /`         | 注释 / 取消注释当前行     |暂时屏蔽一段代码进行调试。|
| `Alt + ↑↓`         | 上下移动当前行          |调整代码逻辑顺序时极度好用。 |
| `Ctrl + D`         | 选中下一个相同词（批量改名神器） |重命名变量或修改多处代码的神器。 |
| `F5`               | 运行 / 调试代码        | 按下 F5 配合断点，你可以让程序停在报错的那一行，查看那一刻所有变量的真实取值。|
| `Shift + Alt + F`  | 格式化代码            |当你从 ChatGPT 或 Copilot 复制了一段代码，发现缩进、空格和括号极其凌乱时，按一下这个键，代码会瞬间变得整齐划一。 |

>💡 **提示**：熟练使用快捷键能大幅提升开发效率

---

<div align="center">

[🏠 返回目录](./index.md) | [⏭️ 下一章：1.4 实战：从零跑通第一个标准化项目 (10 步法)](./04-project-init.md)

</div>