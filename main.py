import re
import time
from urllib.parse import urlparse

import eel


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""

    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "https://" + url

    return url


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


@eel.expose
def validate_url(url: str):
    normalized = normalize_url(url)

    if not normalized:
        return {
            "ok": False,
            "message": "URL 不能为空。"
        }

    if not is_valid_url(normalized):
        return {
            "ok": False,
            "message": "请输入合法的 URL，例如 https://example.com"
        }

    return {
        "ok": True,
        "normalized_url": normalized
    }


@eel.expose
def analyze_url(url: str):
    normalized = normalize_url(url)

    if not is_valid_url(normalized):
        return {
            "status": "error",
            "message": "无法分析该 URL，请检查输入格式。"
        }

    # 模拟分析耗时
    time.sleep(1.6)

    parsed = urlparse(normalized)
    domain = parsed.netloc
    path = parsed.path if parsed.path else "/"

    mock_result = {
        "status": "success",
        "url": normalized,
        "title": f"Analysis for {domain}",
        "summary": (
            "该页面看起来是一个可供 Agent 进一步抓取和理解的网页入口。"
            "从当前 URL 结构来看，页面具备明确的来源域名和可分析路径，适合后续进行内容摘要、结构识别、风险提示与操作建议生成。"
        ),
        "meta": {
            "domain": domain,
            "path": path,
            "captured_at": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "findings": [
            "URL 结构清晰，适合作为抓取入口。",
            "页面来源域名可被用于可信度与上下文判断。",
            "后续可扩展为正文抽取、关键词提炼和语义总结。",
            "适合接入多阶段 Agent 流程：抓取、解析、推理、输出。"
        ],
        "sections": [
            {
                "name": "Source Context",
                "description": "页面来源与 URL 基本信息，可作为后续分析的上下文输入。"
            },
            {
                "name": "Content Summary",
                "description": "对页面核心主题进行摘要，适合放在结果页顶部。"
            },
            {
                "name": "Structural Analysis",
                "description": "对页面标题层级、主体内容区和关键模块进行结构拆解。"
            },
            {
                "name": "Actionable Recommendations",
                "description": "基于分析结果给出下一步建议，例如继续抓取、比对来源、生成报告等。"
            }
        ],
        "recommendations": [
            "接入真实网页抓取模块，返回页面标题、正文和元数据。",
            "增加 Agent 多步骤日志区，展示抓取与推理过程。",
            "加入可折叠的结构化分析面板，提高可读性。",
            "后续支持导出报告、复制摘要和重新分析。"
        ]
    }

    return mock_result


def main():
    eel.init("web")
    eel.start(
        "index.html",
        size=(1200, 750),
        position=(100, 40),
        disable_cache=True,
        port=8587
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已退出。")