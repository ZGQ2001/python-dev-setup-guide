# 1.4 实战：从零跑通第一个标准化项目 (10 步法)
>💡 本章目标：通过一次完整的“实战演习”，掌握从本地创建、环境初始化、自动化配置到云端存档的全流程。

在完成了基础环境的搭建后，我们将通过一个实战项目来巩固所学知识，并建立起一个符合现代开发规范的 Python 项目结构。

本次使用的工具链是 `uv`，它是目前 Python 社区推荐的现代化依赖管理和环境隔离工具。

这是整本手册中含金量最高的一章。我们将通过这“10 步法”，把你从一个“写代码的散户”，直接拉升到“工业级工程开发者”的标准线。

---

> ✅ **官方推荐使用 `uv init` + `uv add` + `uv sync` + `uv run` 现代化工作流**，靠 `pyproject.toml` 和 `uv.lock` 管理依赖，比传统的 `requirements.txt` 更可靠。


### pyproject.toml 和 uv.lock 的区别

这两个文件都要上传，但作用不同：

|文件              |作用                |谁来写           |例子                                 |
|----------------|------------------|--------------|-----------------------------------|
|`pyproject.toml`|**声明需要哪些库**（人读）   |你（通过 `uv add`）|`pandas, openpyxl, python-docx`    |
|`uv.lock`       |**锁定具体到补丁版本**（机器读）|uv 自动生成       |`pandas==2.1.4, openpyxl==3.1.2...`|

**为什么要两个文件？**

`pyproject.toml` 只说”我需要 pandas”，不限定版本。如果只靠它还原环境，A 电脑装到 `pandas 2.1`，半年后 B 电脑装就可能是 `pandas 2.5`，可能引入兼容问题。

`uv.lock` 把所有库（包括库的库）的精确版本号锁死。`uv sync` 时严格按 lock 文件还原，保证所有电脑环境**一字不差**。

### 流程总览

```
第 1 步  D:/CodeProjects/ 下进入纯英文路径
第 2 步  uv init 初始化项目（自动生成项目骨架）
第 3 步  VS Code 打开文件夹
第 4 步  uv add 添加所需库（自动创建 .venv 并锁定版本）
第 5 步  VS Code 选择 Python 解释器
第 6 步  代码质量基建与自动化规范
第 7 步  完善 .gitignore
第 8 步  完善 README.md
第 9 步  在 GitHub 新建仓库（注意 Private/Public 选择）
第 10 步  git init → add → commit → push
```
---

## 第 1 步：进入项目目录

打开终端，进入 `D:/CodeProjects/` 目录（如果没有这个目录，先在 D 盘根目录下创建一个名为 `CodeProjects` 的文件夹）。

```PowerShell
cd D:/CodeProjects/
``` 
>**⚠️ 核对：** 确保你的路径里没有“桌面”、没有“中文”、没有“空格”。如果路径不符合要求，`uv` 可能会报错，或者生成的环境无法被 VS Code 识别。

---

## 第 2 步：初始化项目
>⚠️ 新手必看：在敲下初始化命令前，你必须决定这个项目的“体量”。架构选错，后期极易引发模块导入混乱的玄学报错。

根据项目规划，这里提供两种初始化模式。**强烈建议业务类、工具类项目一律采用模式二。**（除非你明确知道自己在写一个纯算法库，才选模式一）**

这次我们将创建一个名为 `my-first-tool` 的项目。

### 模式一：扁平布局（Flat Layout）

适合：**一次性的几十行数据处理脚本**、不需要打包分享的自用小工具。

终端运行：

```PowerShell
uv init my-first-tool     # my-first-tool 是项目文件夹的名字，随你喜欢取什么名字，但建议全英文、无空格。
cd my-first-tool         # 进入项目文件夹   
```
执行后 uv 会自动生成以下文件：

```
my-first-tool/
├── .python-version       ← 自动指定 Python 版本
├── .gitignore            ← uv 已自动写入基础规则
├── README.md             ← 项目说明模板
├── main.py               ← 示例入口文件
└── pyproject.toml        ← 项目配置（依赖记录在这里）
```

### 模式二：工程布局（src-layout）—— 🌟 强烈推荐

适合：**需要长期维护的项目、包含多个自定义模块、未来准备编译打包成 .exe 桌面软件的工程。**

终端运行：

```PowerShell
# --lib 参数会强制生成工业标准的 src-layout 布局
uv init --lib my-first-tool  
cd my-first-tool               # 进入项目文件夹
```

执行后 uv 会自动生成以下文件：

```
my-first-tool/
├── .python-version
├── pyproject.toml        ← 项目配置（自动配置了打包构建系统）
└── src/                  ← ！！！核心变化在这里！！！
    └── bridge_check/     ← 你的专属代码包（业务逻辑全放这里）
        ├── __init__.py   ← 声明这是一个正规的 Python 包
        └── py.typed
```

- **优点 1（物理隔离）**： 代码在 src/ 下，配置文件在根目录，清晰解耦。

- **优点 2（杜绝导包灾难）**： 强制你使用绝对路径导入（例如 from bridge_check.utils import reader），彻底解决当前目录文件与第三方库重名导致的玄学报错。

- **优点 3（测试与分发）**： 这是 Python 业界最推崇的标准格式，完美兼容未来的单元测试（pytest）和二进制编译（PyInstaller）

>💡 后续操作提醒： 如果你选择了**模式二**，uv 不会自动生成 `main.py`。你需要手动在 `src/bridge_check/` 目录下新建 `main.py` 作为程序入口。

>💡 这些文件除 `.venv/`（暂时还没生成）之外都需要上传到 GitHub。

---

## 第 3 步：VS Code 打开文件夹

VS Code 打开文件夹有三种方式:

1. 直接输入 `code .`，这是最高效的衔接方式。

2. 在项目文件夹上点击右键，选择 "通过 Code 打开" 。

3. 打开 VS Code，选择 "文件" → "打开文件夹"，然后浏览到你的项目目录。

这次主要讲第一种方式，因为它是最直接的命令行到编辑器的衔接，能让你养成习惯。

终端运行：

```PowerShell
# 确保你的环境变量里已经配置了 code 命令（VS Code 安装时默认会添加，如果没有，可能需要手动添加到 PATH）
code .      # 这个命令会让 VS Code 直接打开当前目录（也就是你的项目文件夹）
```

>⚠️ **首次打开必弹窗**： 新手第一次使用 `code .` 打开文件夹时，VS Code 会弹出提示："**是否信任此工作区中的作者？(Do you trust the authors...)**" 必须勾选并点击 "**是，我信任此作者**"，否则代码无法运行且很多功能受限。很多新手因为害怕而点否，导致后续调试报错。

>💡 小技巧：多项目切换 `Ctrl + R`   
>当你已经打开了一个项目，但突然需要查看另一个项目（比如要翻阅之前的《桥梁检测规范》代码）时，不需要关闭软件：
>1. 按下 `Ctrl + R`。
>2. VS Code 会弹出一个最近打开过的项目列表。
>3. 输入关键词或直接回车，即可在当前窗口快速覆盖切换，或按 `Ctrl + Enter` 在新窗口打开。

---

## 第 4 步：添加项目依赖

根据需要安装库，以下是处理 Office 文件的常用组合：

```PowerShell
uv add python-docx openpyxl pandas pypdf python-dotenv   # 这行命令会同时安装这几个库，并自动生成 .venv 环境和 uv.lock 锁定文件
``` 

<div align="center">

|库名             |用途            |
|---------------|--------------|
|`python-docx`  |读写 Word 文档    |
|`openpyxl`     |读写 Excel 文件   |
|`pandas`       |表格数据处理分析      |
|`pypdf`        |读取 PDF 文件     |
|`python-dotenv`|读取 `.env` 配置文件|

</div>


> ✅ **第一次执行 `uv add` 时 uv 会自动做几件事**：
> 
> 1. 检查并下载安装项目需要的 Python 版本（按 `.python-version` 指定的，如果还没装）
> 2. 创建 `.venv` 虚拟环境
> 3. 把依赖记录到 `pyproject.toml`
> 4. 生成或更新 `uv.lock` 锁定具体版本号
> 
> 这一条命令搞定一切，不需要再手动 `uv venv` 或 `uv pip freeze`。

---

## 第 5 步：选择 Python 解释器

VS Code 需要知道你项目的 Python 环境在哪里，才能正确运行和调试代码。

在 VS Code 中，按下 `Ctrl+Shift+P` 打开命令面板，输入 `Python: Select Interpreter`，然后选择你项目目录下的 `.venv` 里的 Python 解释器。

>⚠️ **如果你在这里没有看到 `.venv` 选项，说明 uv 没有正确创建虚拟环境，或者 VS Code 没有正确识别到它。请回到第 4 步检查 `uv add` 是否成功执行，并确保你的项目目录结构正确。**

**为什么必须做这一步？**

VS Code 里可能同时存在多个 Python：系统全局的、各个项目的 `.venv`、其他工具自带的。VS Code 不知道你想用哪个跑代码，需要你**手动指定**。

选了正确的 `.venv` 之后，VS Code 才知道：

- 跑 `python xxx.py` 时该用哪个 Python
- 代码里 `import pandas` 时去哪个文件夹找库
- 智能提示从哪里读取库的函数列表

> ⚠️ 没选对的典型现象：明明 `uv add pandas` 装好了，VS Code 却在 `import pandas` 下画红线提示”找不到模块”——其实是用错 Python 了。

---

## 第 6 步：代码质量基建与自动化规范

在多人协作或长期维护的项目中，代码风格不一致（空格乱敲、变量乱命名、无用导入）会导致极高的维护成本。靠人工检查是徒劳的，必须通过底层工具进行强制约束，做到**严禁带红线（报错和警告）提交**。

### 1. 区分“运行依赖”与“开发依赖”

在安装代码检查工具之前，必须先理解依赖的分级概念：

- 运行依赖（标准 add）：例如 pandas, pyside6。这些是程序运行不可或缺的库。未来打包成 .exe 时，这些库必须被一起打包。

- 开发依赖（加 --dev 参数）：例如 ruff（代码检查）, pytest（单元测试）。这些只是你在开发阶段用来辅助你的“施工工具”，程序真正交付运行或打包时，完全不需要它们。

#### 操作命令：

在项目根目录（VS Code 终端）执行以下命令，专门安装开发工具：

```bash
uv add --dev ruff pytest
```

> 💡 底层变化： 执行后打开 pyproject.toml，你会发现这些库被单独记录在了 [tool.uv] 或 [project.optional-dependencies] 相关的开发依赖区块中，实现了工具与业务的彻底物理隔离。

### 2. 在 VS Code 中配置 Ruff 自动化

先前在1.3节我们已经安装了 Ruff 插件，现在我们要让它在每次保存代码时自动检查并修复问题。

此处不过多赘述，具体配置方法请参考 1.3 节的 `settings.json` 配置部分。

**传送门**： [VS Code 配置详解](./03-github-ssh.md#4-settingsjson-配置)

### 3. 定义项目的“红线规则”

不同项目对代码的严格程度要求不同。我们需要在项目的配置文件中立下规矩。

打开项目根目录的 `pyproject.toml` 文件，在最底部追加以下内容：

```ini, TOML
# ====== Ruff 规则配置区块 ======
[tool.ruff]
# 设定代码一行的最大长度。超过此长度 Ruff 会自动帮你换行，避免横向滚动条过长
line-length = 100 
# 设定需要检查的源代码目录，排除虚拟环境等无关文件
src = ["src", "tests"]

[tool.ruff.lint]
# 选择要启用的检查规则集
select = [
    "E",  # pycodestyle 错误（如缩进、空格不规范）
    "F",  # Pyflakes（如定义了变量却没使用、引入了没用的库）
    "I",  # isort（import 排序规范）
    "W",  # pycodestyle 警告
]
# 忽略某些特定的规则（如果你觉得某条规则太严厉，可以把它的编号写在这里）
#例如可修改为 ignore = ["RUF001", "RUF002", "RUF003"]（明确忽略易混淆字符（中文标点）规则，防止误报）
ignore = []
```

### 4. 日常开发纪律

完成以上配置后，你的开发体验会发生质的改变：

1. **自动清理**：如果你引入了 `import os` 但整篇代码都没用到，一按保存（`Ctrl+S`），这行代码会被 Ruff 瞬间自动删掉。

2. **强制对齐**：随意打乱的函数参数缩进，保存瞬间会自动排列整齐。

3. **红线拦截**：VS Code 编辑器里如果出现红色或黄色波浪线，必须当场解决，绝对不允许带着波浪线执行 git push 上传代码。

你现在已经在 pyproject.toml 里配置好了就则。接下来可以试试看：

1. 在 `src` 目录下写一段故意违反规则的代码（比如一行写 200 个字符，或者引入一个没用的 `import os`）。

2. 按下 `Ctrl + S`，看它是否自动帮你删除了无用引用，并把长代码切成了两行。

---

## 第 7 步：完善 .gitignore

### .gitignore 工作原理（先理解再写规则）

`.gitignore` 是一份”**这些文件 Git 别管**“的清单。但有个关键限制：

> ⚠️ **`.gitignore` 只对”还没被 Git 追踪过”的文件生效。**

也就是说：

- ✅ **新文件**：写进 `.gitignore` 后 Git 直接无视，不会出现在 `git status` 里
- ❌ **已经 commit 过的文件**：再加进 `.gitignore` 没有任何效果，Git 仍然会追踪它

这就是为什么强调要在**第一次 `git add` 之前**就写好 `.gitignore`。事后补救需要先用 `git rm --cached` 把文件从追踪列表中移除（见后续答疑章节）。

### 完整 .gitignore 模板

打开你的 `.gitignore` 文件（以点开头，无后缀），替换为为以下内容：

```gitignore
# ==========================================
# ✅ 以下文件不在此列表 = 会被上传到 GitHub
# pyproject.toml    → 必须上传（项目配置）
# uv.lock           → 必须上传（依赖版本锁定）
# .python-version   → 必须上传（Python 版本指定）
# .gitignore        → 必须上传
# README.md         → 必须上传
# .env.example      → 建议上传（配置模板）
# *.bat             → 建议上传 （启动脚本）
# 所有 .py 文件     → 必须上传
# ==========================================


# ===== ❌ Python 虚拟环境（体积大，必须忽略）=====
# .venv 是 uv 创建的虚拟环境文件夹，里面是按项目装的所有库
# 体积可达几百 MB，且每台电脑应该自己重新生成（uv sync）
.venv/
venv/
__pycache__/        # Python 运行时自动生成的字节码缓存
*.py[cod]           # 编译后的 Python 文件
*.pyo
*.egg-info/
dist/
build/
.eggs/

# ===== ❌ 敏感配置（含密码/密钥，绝对不能上传）=====
.env
.env.local
.env.production
config.ini
secrets.json
*.key
*.pem
*.p12

# ===== ❌ 系统垃圾文件 =====
.DS_Store           # Mac 系统在每个文件夹自动生成的隐藏文件
Thumbs.db           # Windows 缩略图缓存
desktop.ini         # Windows 文件夹自定义图标配置

# ===== ❌ VS Code 本地配置 =====
.vscode/
*.code-workspace

# ===== ❌ 日志与临时文件 =====
*.log
*.tmp
*.temp
/temp/
/cache/
/output/

# ===== ❌ WPS / Office 临时锁定文件 =====
# 当你在 WPS 或 Office 打开 report.docx 时，
# 系统会同时生成一个 ~$report.docx 隐藏文件，
# 用来标记"这个文档正在被编辑"。
# 关闭文档后通常会自动删除，但偶尔会残留。
# 这些临时文件不是你的内容，不应该上传。
~$*.docx
~$*.xlsx
~$*.pptx
~$*.doc
~$*.xls

# ===== ❌ 大体积数据文件（GitHub 单文件限制 100MB）=====
# 按需取消注释：
# *.csv
# *.xlsx
# *.pdf
# /data/
```

### 验证 .gitignore 是否生效

写完规则后执行：

```bash
git status
```

**看不到的文件就是被忽略成功的。** 例如 `.venv/` 没出现在列表里，说明规则生效。

如果某个文件应该被忽略但仍出现在 `git status` 里：

- 检查 `.gitignore` 拼写是否正确
- 该文件可能已被 Git 追踪（见下方”补救方法”）

> 💡 这一步非常重要，必须在第一次 `git add` 之前完成——`.gitignore` 只对尚未追踪的文件生效，以后再补就晚了。

---

## 第 8 步：完善 README.md

`uv init` 生成了空的 `README.md`，参考以下模板填写：

```markdown
# 项目名称

一句话说明这个项目是干什么的。

## 功能

- 功能 1
- 功能 2

## 快速开始

# 克隆项目
git clone git@github.com:用户名/仓库名.git
cd 仓库名

# 一键还原依赖（自动创建 .venv 并安装所有库）
uv sync

# 运行
uv run main.py

## 配置
复制 `.env.example` 为 `.env`，填入你的配置信息。
```


## 第 9 步：在 GitHub 新建仓库

GitHub 网页右上角 `+` → `New repository`：

- **Repository name**：和本地文件夹同名
- **Private vs Public**：⚠️ **重要选择**
  - 🔒 **Private**（私有）：只有你能看到。**涉及公司数据、检测项目、客户信息的必须选这个**
  - 🌐 **Public**（公开）：全网可见。开源项目、个人作品集才选这个
- **不要勾选**任何初始化选项（不要勾 README、.gitignore、license）

---

## 第 10 步：上传到 GitHub

当你完成了第 9 步在网页上创建仓库后，你会看到一个带有代码指令的“空仓库”页面。

### 1. 优先复制 GitHub 提供的指令

不要试图手动输入远程仓库地址。请直接在 GitHub 网页上找到 `…or push an existing repository from the command line` 这一栏。

点击该区块右上角的“复制”图标，直接在你的 **Git Bash** 中粘贴运行。这样可以 100% 确保仓库地址（SSH 地址）是正确的。

### 2. 标准指令解析

如果你选择**手动分步**执行，请在终端依次输入以下命令：

```bash
# 1. 初始化本地 Git 仓库（让这个文件夹变为可追踪状态）
git init

# 2. 将当前目录下所有文件添加到“待提交区”
git add .

# 3. 签署提交说明（双引号内是本次改动的注释，必须写）
git commit -m "初始化项目"

# 4. 强制指定主分支名为 main（符合现代 GitHub 标准）
git branch -M main

# 5. 建立本地与云端仓库的关联（建议从 GitHub 页面直接复制此行）
git remote add origin git@github.com:用户名/仓库名.git

# 6. 正式推送：将本地代码“发射”到云端
git push -u origin main
```
### 3. 连通标准

- 终端反馈：如果你看到 `branch 'main' set up to track 'origin/main'`，说明链路已通。
- 网页反馈：刷新 GitHub 仓库页面，你原本“空空如也”的页面现在应该已经显示出了 `src` 文件夹、`pyproject.toml` 等文件。

---

## 🏆 第一部分总结：你已经跨过了门槛

#### 恭喜你！到这一步为止，你已经不仅是在“写代码”，而是在“构建工程”。

- 你拥有了物理隔离的环境（uv）。

- 你拥有了自动纠错的守卫（Ruff）。

- 你拥有了多端同步的保险箱（GitHub）。

#### 第一章正式完结。现在，你的 GitHub 仓库里是不是已经躺着一份整齐的项目代码了？

#### 下一步预告

地基已固，繁花将起。在接下来的第二章节中，我们会把“Git 三连”精简为一套“肌肉记忆”，并教你如何开始一段标准开发工作流。

---

<div align="center">

[🏠 返回目录](./index.md) | [⏭️ 下一章：2.1 日常代码提交流程](./05-workflow.md)

</div>


