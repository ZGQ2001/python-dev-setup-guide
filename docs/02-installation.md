# 1.2 基础环境安装

> 💡 **本章目标**：完成基础软件的安装，并确立物理硬盘上的工程规范。这一阶段的操作，通常在新电脑上只做一次。

## 一、 项目路径与命名（极其重要）

在下载任何软件之前，你必须先在电脑中划出一块“绝对纯净”的作业区。

### 1. 项目路径

> ⚠️ **桌面建项目是最常见的新手错误，必须从一开始就杜绝。**

很多中文用户桌面的真实路径是 `C:\Users\用户名\Desktop\`，含中文、含空格，双重违规。

- ❌ `C:\Users\用户名\桌面\我的项目\`  → 中文路径，必出问题
- ❌ `C:\Users\用户名\Desktop\bridge check\`  → 含空格，必出问题
- ❌ `D:\代码项目\2026年\数据\`  → 中文路径，必出问题
- ✅ `D:\CodeProjects\bridge-check\`  → 纯英文，无空格，正确

**为什么这么严格？**

很多 Python 库（尤其是 Office 处理库）在路径含中文或空格时会报奇怪的编码错误，排查极难。直接禁用这两类字符可以省掉 90% 的玄学问题。

**打开你的 D 盘（或除 C 盘外的非系统盘），新建一个名为 `CodeProjects` 文件夹，以后你所有的学习、练习和正式项目，必须全部放在这个目录下。**

---

### 2. 项目命名规范

文件夹名和 GitHub 仓库名应该保持一致，遵循以下规则：

- **小写字母**，单词之间用**连字符** `-` 分隔（kebab-case）
- **见名知意**，避免 `test`、`new`、`xiangmu1`、`untitled` 这种无意义命名
- 工具类项目可加后缀：`-tool`、`-cli`、`-gui`

<div align="center">

|❌ 不推荐         |✅ 推荐                     |说明        |
|--------------|-------------------------|----------|
|`test1`       |`bridge-detection-report`|见名知意      |
|`MyProject`   |`my-project`             |全小写更通用    |
|`bridge_check`|`bridge-check`           |连字符比下划线更主流|
|`项目1`         |`road-survey-2024`       |不用中文      |
</div>

> 💡 当你有十几个项目时，规范的命名能让你 3 秒钟找到目标，而不是一个个点开看。

---

### Git Bash 里的路径斜杠

Windows 系统用反斜杠 `\`，但 **Git Bash 用正斜杠 `/`**：

```bash
# ❌ Git Bash 里反斜杠会报错
cd D:\CodeProjects

# ✅ Git Bash 里用正斜杠
cd D:/CodeProjects
```

> 在 VS Code 的 Git Bash 终端里写命令，路径一律用 `/`。Python 代码里也建议统一用 `/`，跨平台兼容。   
>
> 💡 **Git Bash 粘贴技巧：** 在 Git Bash 终端中，`Ctrl+V` 是特殊控制符无法粘贴，粘贴请使用 **`Shift+Insert`** 或点击鼠标右键。
---

### 3. 相对路径 vs 绝对路径

代码里引用文件时，**绝对路径**写死了电脑位置，换电脑就报错：

```python
# ❌ 绝对路径：只在你自己电脑上能跑
df = pd.read_excel("C:\\Users\\用户名\\Desktop\\data.xlsx")
```

**相对路径**以项目文件夹为起点，换电脑也能用：

```python
# ✅ 相对路径：./data/data.xlsx 表示项目文件夹内的 data 子文件夹
df = pd.read_excel("./data/data.xlsx")
```

推荐的项目文件结构:

```
my-project/
├── .venv/                  ← 虚拟环境（自动生成，不要上传）
├── .python-version         ← 锁定 Python 版本
├── pyproject.toml          ← 核心配置文件
├── README.md
└── src/                    ← ！！！所有业务代码必须放在这里！！！
    └── my_project/         
        ├── __init__.py     ← 标识这是一个标准的 Python 包
        └── py.typed        ← 声明支持静态类型推导
```
> 养成用相对路径的习惯，代码上传 GitHub 后别人克隆也能直接运行。
>
>💡此项目文件结构后续会有专门章节讲解，这里先给个大致框架，强调所有业务代码必须放在 src 文件夹里，避免和配置文件、文档等混在一起。

---

## 二、 基础软件安装：构建标准工作环境

请依次下载并安装以下两个核心组件并注册GitHub账号。

**Git**

- 下载地址：https://git-scm.com/download/win
- 安装时全部默认选项，一路 `Next` 即可
- 安装完成后，在电脑任意位置点击右键，如果菜单中出现了 `Git Bash Here`，说明安装成功

**VS Code**

- 下载地址：https://code.visualstudio.com/
- 安装时勾选 “添加到 PATH” 和 “添加到右键菜单”，其余默认
- 安装完打开，界面是英文属正常，后面装插件汉化

**注册GitHub 账号**

- 注册地址：https://github.com/
- 用常用邮箱注册，用户名只用英文和数字

---

## 三、 Python 引擎：安装 uv 包管理器

在现代 Python 开发中，我们不再直接从官网下载安装包，而是使用 uv。它是目前全球最快的 Python 包管理工具，集成了 Python 版本管理、虚拟环境创建和依赖安装功能。

### 1. 前置条件：解除 PowerShell 脚本执行限制   

在安装 uv 之前，必须在你的新电脑上执行此操作，否则后续无法激活虚拟环境。

1. 在开始菜单搜索 PowerShell，右键选择“以管理员身份运行”。

2. 输入以下命令并回车：

```powershell
 Set-ExecutionPolicy RemoteSigned -scope CurrentUser
```
3. 看到提示后输入 `Y` 并回车。

**为什么要这么做？**

Windows 出于安全考虑，**默认禁止 PowerShell 执行任何 `.ps1` 脚本**——防止有人骗你下载并双击恶意脚本。但虚拟环境激活、uv 安装等操作都需要执行 `.ps1` 脚本。

`RemoteSigned` 是一个折中策略：

- ✅ 本地写的脚本可以直接运行（你自己的虚拟环境激活脚本）
- ✅ 网络下载的脚本必须经过数字签名才能运行（防止恶意脚本）

`-scope CurrentUser` 表示只对当前用户生效，不影响其他用户，更安全。

>不执行这步的后果：激活 `.venv` 时报错 `无法加载文件，因为在此系统上禁止运行脚本`。
### 2. 推荐安装方式：官方独立安装

这种方式不依赖你系统中是否已经有 Python，是最纯净的安装路径。

在上述打开的 PowerShell 窗口中，直接粘贴并运行以下命令：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安装完成后，必须关闭并重新打开终端，输入以下命令验证：

```powershell
uv --version
```

如果看到版本号输出（如 `uv 0.x.x`），说明引擎已就绪。

### 3. 备选方式：通过 pip 安装

如果你已经安装了 Python，并且 `pip` 可用，也可以通过 pip 安装 uv：

```bash
pip install uv
```

### 4. 使用 uv 极速安装 Python

有了 `uv`，你再也不需要去 Python 官网找安装包，更不需要手动配置复杂的“系统环境变量”。

在终端输入以下命令，安装目前最稳定的生产版本：

```bash
uv python install 3.12.13
```
安装完成后，输入 `uv python list` 可以看到已安装的 Python 版本列表，确认 `3.12.13` 在列即可。

>💡同时存在多个 Python 版本
>
>uv 会自动下载并管理不同版本的 Python。这意味着你的电脑可以同时存在 3.10、3.11、3.12 等多个版本，而每个项目都可以通过 .python-version 文件精准指定自己需要的版本，互不干扰。

---

## 四、 本章操作自检清单
在进入下一章之前，请确保你已经完成了以下动作：

[ ] 路径确认：已经在 D 盘（或非系统盘）建立了 D:/CodeProjects 文件夹。

[ ] Git：右键菜单可见 Git Bash Here。

[ ] VS Code：已安装并勾选了“添加到右键菜单”。

[ ] GitHub：已拥有账号且用户名符合纯英文规范。

[ ] uv 引擎：在终端输入 uv --version 能正常显示版本。

[ ] Python：已通过 uv python install 3.12 完成了工作环境部署

---

<div align="center">

[🏠 返回目录](./index.md) | [⏭️ 下一章：1.3 GitHub 联动与编辑器初步调优](./03-github-ssh.md)

</div>