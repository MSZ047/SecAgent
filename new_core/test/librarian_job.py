import os
import json
from pathlib import Path
from langchain_openai import ChatOpenAI
from app.config.settings import settings
import re
def run_refactoring(wiki_dir: str = "./llmwiki"):
    llm = ChatOpenAI(model="MiniMax-M2.5", api_key=settings.minimax_api_key, base_url="https://api.minimaxi.com/v1")
    wiki_path = Path(wiki_dir)
    dirty_file = wiki_path / "dirty_pages.json"
    
    if not dirty_file.exists():
        print("没有需要重构的页面。")
        return

    dirty_pages = json.loads(dirty_file.read_text(encoding="utf-8"))
    
    for page_name in dirty_pages:
        page_path = wiki_path / page_name
        if not page_path.exists(): continue
            
        print(f"🔄 正在重构整理: {page_name}...")
        raw_content = page_path.read_text(encoding="utf-8")
       
        prompt = f"""
        你是一个严谨的技术文档编辑。
        以下是一个 Markdown 文件的全部内容，由于白天被多次追加写入，里面可能存在逻辑重复、排版混乱、甚至互相冲突的内容。
        
        请你重新梳理这份文档：
        1. 消除重复的段落和冗余的说明。
        2. 将散落的知识点分类整合为清晰的层级结构（如：原理、操作步骤、代码示例等）。
        3. 保持原意不变，不丢失任何核心数据。
        4. 静默处理，不要在文本或者目录里面出现已更新的字眼
        原始文档内容：
        ---
        {raw_content}
        ---
        
        请直接输出重构后完美排版的 Markdown 内容，不要有任何多余的开头或结尾。
        """
        raw = llm.invoke(prompt).content
        clean_content = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
        # 覆写原文件
        page_path.write_text(clean_content, encoding="utf-8")
        
    # 清空待处理列表
    dirty_file.unlink()
    print("✨ 所有脏页面重构完成！")

if __name__ == "__main__":
    run_refactoring()