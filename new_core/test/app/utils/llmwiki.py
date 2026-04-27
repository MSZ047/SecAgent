import re
import json
from pathlib import Path
from datetime import datetime
from langchain_openai import ChatOpenAI
from app.config.settings import settings

class LLMWikiManager:
    def __init__(self, wiki_root: str = "./llmwiki"):
        self.wiki_root = Path(wiki_root)
        self.wiki_root.mkdir(parents=True, exist_ok=True)
        self.index_file = self.wiki_root / "index.md"
        self.log_file = self.wiki_root / "log.md"
        
        if not self.index_file.exists(): self._init_index()
        if not self.log_file.exists(): self._init_log()

        # 使用推理能力更强的模型（如 DeepSeek-R1 或 MiniMax-M2.5）
        self.llm = ChatOpenAI(
            model="MiniMax-M2.5", 
            api_key=settings.minimax_api_key,
            base_url="https://api.minimaxi.com/v1",
        )

    def _init_index(self):
        self.index_file.write_text("# 知识库索引 (Index)\n\n## 核心实体与概念\n\n## 最近更新\n", encoding="utf-8")

    def _init_log(self):
        self.log_file.write_text("# 变更日志 (Log)\n\n", encoding="utf-8")

    def _log_event(self, action: str, details: str):
        """按时间顺序记录操作"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"## [{timestamp}] {action} | {details}\n"
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(entry)

    def _clean_think_tags(self, text: str) -> str:
        """无情斩断思考过程，只保留知识干货"""
        cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        return cleaned.strip()
    
    def read_wiki_page(self, page_name: str) -> str:
        """读取指定的 wiki 页面内容"""
        file_path = self.wiki_root / page_name
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        else:
            return f"提示：页面 '{page_name}' 不存在，请尝试查阅其他页面或直接进行下一步。"

    def ingest(self, raw_content: str, source_url: str):
      
        current_index = self.index_file.read_text(encoding="utf-8")
        
        # 步骤 1：制定重构计划
        plan_prompt = f"""
        你现在是 LLM Wiki 的知识库管理员。
        当前维基索引内容如下：
        {current_index}

        现在有一个新的来源内容：
        {raw_content}
        来源地址：{source_url}

        你的任务是分析这个新来源，并制定一个更新计划。请输出一个 JSON 格式的指令列表：
        【极度重要：页面合并原则】
        1. 你必须逐一检查新内容中的核心概念，并与当前的维基目录进行严格比对。
        2. 如果新概念在目录中已经有语义相同或高度相关的页面（例如，你想写“概念A_扩展”，但目录已有“概念A”），你 **绝对禁止** 使用 "create" 创建新页面！你 **必须** 使用 "update" 将内容追加到已有的页面中。
        3. 只有当一个概念在目录中 100% 找不到任何相关项时，才允许使用 "create"。
        4. "filename" 必须完全匹配目录中已有的文件名（不区分大小写）。
        请严格按照此格式输出 JSON（不要包含 think 标签）：
        {{
            "operations": [
                {{"action": "create", "filename": "文件名.md", "content": "完整的 Markdown 内容"}},
                {{"action": "update", "filename": "文件名.md", "append_content": "要补充的内容"}}
            ]
        }}
        """
        
        # 强制模型输出 JSON 计划
        raw_plan = self.llm.invoke(plan_prompt).content
        plan_str = self._clean_think_tags(raw_plan)
        
        try:
            # 兼容模型输出带 ```json 的情况
            json_str = re.search(r'\{.*\}', plan_str, re.DOTALL).group()
            plan = json.loads(json_str)
        except Exception as e:
            print(f"❌ 计划解析失败: {e}。原始输出: {plan_str}")
            return

        # 步骤 2：执行计划 (一个源影响多个源)
        modified_pages = []
        for op in plan.get("operations", []):
            action = op["action"]
            filename = op["filename"].lower().replace(" ", "_") # 强制规范化文件名
            file_path = self.wiki_root / filename

            if action == "create":
                if file_path.exists():
                    # 终极兜底：如果模型犯傻非要 create 存在的页面，强制转为 update
                    current_txt = file_path.read_text(encoding="utf-8")
                    file_path.write_text(current_txt + "\n\n### 新增补充\n" + op.get("content", ""), encoding="utf-8")
                else:
                    file_path.write_text(op["content"], encoding="utf-8")
                modified_pages.append(filename)
                
            elif action == "update":
                if file_path.exists():
                    current_txt = file_path.read_text(encoding="utf-8")
                    file_path.write_text(current_txt + "\n\n### 补充更新\n" + op["append_content"], encoding="utf-8")
                    modified_pages.append(filename)

        # 【重构点 3】记录状态给“后台图书管理员”
        self._record_dirty_pages(modified_pages)
        self._log_event("ingest", f"从 {source_url} 处理了 {len(plan.get('operations', []))} 个动作")
        print(f"✅ 摄取完成。")

    def _record_dirty_pages(self, pages: list):
        """记录今天被追加过内容的页面，留给夜间重构任务"""
        state_file = self.wiki_root / "dirty_pages.json"
        existing = []
        if state_file.exists():
            existing = json.loads(state_file.read_text(encoding="utf-8"))
        
        updated_state = list(set(existing + pages))
        state_file.write_text(json.dumps(updated_state), encoding="utf-8")