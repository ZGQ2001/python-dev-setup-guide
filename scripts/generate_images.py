"""
一键生成 docs/assets/images/ 下所有 Mermaid 配图。

用法：uv run python scripts/generate_images.py

原理：将 Mermaid 文本 → Base64 编码 → 拼入 mermaid.ink API → 下载 PNG。
每张图内置超时保护（15 秒）+ 最多 3 次重试 + 友好中文报错。
"""

import base64
import time
import sys
from pathlib import Path
import requests

# Windows Cmd 默认 GBK，强制 UTF-8 输出防止中文/emoji 乱码
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ============================================================
# 输出目录
# ============================================================
OUT_DIR = Path("docs/assets/images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 重试下载函数
# ============================================================
def download_mermaid(mermaid_code: str, filename: str, width: int = None):
    """
    将 Mermaid 代码转为 PNG 并保存。
    包含超时保护（15 秒）和最多 3 次重试。
    width: 图片宽度（像素），横向流程图建议 1200 以避免挤压。
    """
    # ① 编码 Mermaid 文本 → Base64 → 拼 URL
    b64 = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("utf-8")
    url = f"https://mermaid.ink/img/{b64}"
    if width:
        url += f"?width={width}"

    # ② 下载，带超时和重试
    for attempt in range(1, 4):
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            break  # 成功，跳出循环
        except requests.RequestException:
            if attempt == 3:
                print(f"   ⚠️  网络不太通畅，请检查代理配置或稍后重试。")
                return False
            print(f"   第 {attempt} 次请求失败，2 秒后重试...")
            time.sleep(2)

    # ③ 保存图片
    out_path = OUT_DIR / filename
    out_path.write_bytes(resp.content)
    print(f"   ✅  {filename}  ({len(resp.content) / 1024:.1f} KB)")
    return True


# ============================================================
# Mermaid 图定义
# ============================================================

MERMAID_GRAPHS = {
    # ========== 05 章配图 ==========

    "ch05-vibe-vs-traditional-compare.png": """
graph LR
    subgraph 传统编程
        direction TB
        A1["📖 学语法"] --> A2["⌨️ 亲手敲代码"]
        A2 --> A3{"报错了？"}
        A3 -->|"自己排查修改"| A2
        A3 -->|"跑通了"| A4["✅ 完成"]
    end
    subgraph Vibe Coding
        direction TB
        B1["💬 中文描述需求"] --> B2["🤖 AI 生成代码"]
        B2 --> B3{"目测结果对不对？"}
        B3 -->|"不对"| B4["📋 报错贴回 AI"]
        B4 --> B2
        B3 -->|"对了"| B5["✅ 完成"]
    end
    style A1 fill:#f5f5f5,stroke:#607D8B
    style B1 fill:#E3F2FD,stroke:#2196F3
""".strip(),

    "ch05-ai-tool-decision-flow.png": """
graph TD
    A["🤔 你的需求是什么？"] --> B{"做个 Excel 小工具"}
    A --> C{"逻辑复杂、多步骤"}
    A --> D{"冷门问题、中文搜不到"}
    A --> E{"需要理解长文档"}

    B --> B1["🌟 豆包<br/>中文最顺、生成最快"]
    C --> C1["🧠 DeepSeek<br/>推理能力强、多步骤不翻车"]
    D --> D1["🌍 ChatGPT<br/>英文社区资源最全"]
    E --> E1["📚 Kimi<br/>一次能读几十页"]

    style A fill:#E3F2FD,stroke:#2196F3
    style B1 fill:#C8E6C9,stroke:#4CAF50
    style C1 fill:#C8E6C9,stroke:#4CAF50
    style D1 fill:#C8E6C9,stroke:#4CAF50
    style E1 fill:#C8E6C9,stroke:#4CAF50
""".strip(),

    "ch05-four-step-validation-flow.png": """
graph TD
    A["① 粘贴代码<br/>到 VS Code"] --> B["② 终端运行<br/>uv run main.py"]
    B --> C["③ 目测输出<br/>数量/数值/格式"]
    C --> D{"结果对不对？"}
    D -->|"不对"| E["④ 报错贴回 AI<br/>完整红字 + 一句话"]
    E --> A
    D -->|"对了"| F["✅ 验收通过"]

    style A fill:#E3F2FD,stroke:#2196F3
    style B fill:#E3F2FD,stroke:#2196F3
    style C fill:#FFF9C4,stroke:#FBC02D
    style E fill:#FFCDD2,stroke:#F44336
    style F fill:#C8E6C9,stroke:#4CAF50
""".strip(),

    # ========== 06 章配图 ==========

    "ch06-crime-scene-model-concept.png": """
graph TD
    A["🔍 阅读现场报告<br/>看懂 Traceback"] --> B["📋 提取四条线索<br/>错误类型 + 文件 + 行号 + 原因"]
    B --> C["📝 汇总案件报告<br/>完整红字 + 一句话描述"]
    C --> D["📠 传真给专家<br/>粘贴给 AI"]
    D --> E["🔧 按修复方案还原<br/>替换代码"]
    E --> F["✅ 验证是否告破<br/>重新运行"]

    style A fill:#E3F2FD,stroke:#2196F3
    style F fill:#C8E6C9,stroke:#4CAF50
""".strip(),

    "ch06-three-step-debugging-sop.png": """
graph TD
    A["① 复制红字<br/>100% 完整，一字不漏"] --> B["② 粘贴给 AI<br/>加标准话术"]
    B --> C["③ 替换代码<br/>精准覆盖，不乱改"]
    C --> D{"跑通了吗？"}
    D -->|"没通"| A
    D -->|"通了"| E["✅ 修复完成"]
    F["💡 三轮不成，立刻换 AI"]

    style A fill:#FFCDD2,stroke:#F44336
    style B fill:#E3F2FD,stroke:#2196F3
    style C fill:#FFF9C4,stroke:#FBC02D
    style E fill:#C8E6C9,stroke:#4CAF50
""".strip(),

    "ch06-traceback-anatomy-concept.png": """
graph TD
    A["Traceback (most recent call last)"] --> B["File main.py, line 23<br/>调用了 find_excel_files()"]
    B --> C["File io_handler.py, line 15<br/>raise FileNotFoundError"]
    C --> D["FileNotFoundError:<br/>数据目录不存在：data"]

    D --> E["🔑 规则 1：先看最后一行<br/>错误类型 + 错误原因"]
    D --> F["🔑 规则 2：往上看一行<br/>哪个文件的第几行"]

    style A fill:#ECEFF1,stroke:#607D8B
    style D fill:#FFCDD2,stroke:#F44336
    style E fill:#C8E6C9,stroke:#4CAF50
    style F fill:#C8E6C9,stroke:#4CAF50
""".strip(),

    "ch06-encoding-dictionary-compare.png": """
graph LR
    subgraph "UTF-8 字典"
        direction TB
        A1["字节 0xd4"] --> A2["❌ 没有对应的字"]
        A2 --> A3["乱码！"]
    end
    subgraph "GBK 字典（Windows 中文默认）"
        direction TB
        B1["字节 0xd4"] --> B2["✅ 对应汉字"]
        B2 --> B3["月"]
    end

    style A3 fill:#FFCDD2,stroke:#F44336
    style B3 fill:#C8E6C9,stroke:#4CAF50
""".strip(),

    "ch06-bat-encoding-flow.png": """
graph TD
    A["VS Code 里写 .bat<br/>编码：UTF-8"] --> B["双击运行<br/>启动 Windows Cmd"]
    B --> C["Cmd 默认编码：GBK"]
    C --> D["用 GBK 字典解码 UTF-8 字节"]
    D --> E["屏幕显示：閿熸枻鎷�"]
    E --> F["修复方案：加 chcp 65001"]
    F --> G["✅ 中文正常显示"]

    style D fill:#FFCDD2,stroke:#F44336
    style E fill:#FFCDD2,stroke:#F44336
    style F fill:#FFF9C4,stroke:#FBC02D
    style G fill:#C8E6C9,stroke:#4CAF50
""".strip(),
}


# ============================================================
# 主流程
# ============================================================
def main():
    total = len(MERMAID_GRAPHS)
    success = 0

    print(f"📸 开始生成 {total} 张 Mermaid 配图...")
    print(f"   输出目录：{OUT_DIR.resolve()}")
    print()

    # 横向流程图（graph LR）需要更大宽度，避免文字挤压
    WIDE_GRAPHS = {
        "ch05-vibe-vs-traditional-compare.png",
        "ch06-encoding-dictionary-compare.png",
    }

    for filename, mermaid_code in MERMAID_GRAPHS.items():
        print(f"⬇️  {filename}")
        width = 1200 if filename in WIDE_GRAPHS else None
        if download_mermaid(mermaid_code, filename, width=width):
            success += 1

    print()
    print(f"🎉 完成：{success}/{total} 张图成功生成")
    if success < total:
        print("⚠️  部分图片生成失败，请检查网络后重试。")
        sys.exit(1)


if __name__ == "__main__":
    main()
