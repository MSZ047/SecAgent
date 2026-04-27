from langchain_core.tools import tool
from app.utils.llmwiki import LLMWikiManager

# 全局单例化 Wiki 管理器
wiki_manager = LLMWikiManager()

@tool
def read_wiki(page_name: str) -> str:
    """
    读取本地 Wiki 知识库中的 Markdown 页面。
    当你需要查找攻击 payload、绕过技巧或过往经验时使用此工具。
    建议：如果不确定有哪些文档，请先传入 'index.md' 查看核心目录，或者传入 'log.md' 查看最近的知识演进记录。
    """
    print("模型在调用read_wiki")
    return wiki_manager.read_wiki_page(page_name)

@tool
def submit_to_wiki(raw_content: str, target_url: str) -> str:
    """
    将扫描日志、漏洞发现或测试结果提交给 LLM Wiki 知识库。
    [非常重要] 当你完成对一个网站的测试后，必须调用此工具。它会触发知识库的自动“编译”，大模型会在后台自动重构相关的知识点页面、更新目录和日志。
    参数说明:
    - raw_content: 包含漏洞细节、成功 payload 或测试摘要的原始文本。
    - target_url: 被测试的目标 URL 或测试目标。
    """
    print("模型正在尝试提交wiki")
    # 调用新版的 ingest 方法，触发全局知识重构
    wiki_manager.ingest(raw_content, target_url)
    return "✅ 经验已成功提交！现在请结束扫描，不要再用任何工具，直接输出最终报告。"