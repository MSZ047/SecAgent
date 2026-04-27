import json
import re
from langchain_openai import ChatOpenAI
from app.config.settings import settings

class ReportGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="MiniMax-M2.5", 
            api_key=settings.minimax_api_key,
            base_url="https://api.minimaxi.com/v1",
            temperature=0.1 
        )

    def _extract_json(self, text: str) -> str:
        cleaned = re.sub(r'<think>[\s\S]*?</think>', '', text)
        cleaned = cleaned.replace('```json', '').replace('```', '').strip()
        start = cleaned.find('[')
        end = cleaned.rfind(']')
        if start != -1 and end != -1 and end > start:
            return cleaned[start:end+1].strip()
        return cleaned

    def generate_frontend_json(self, agent_raw_result: str, target_url: str) -> list:
        print("[ReportGenerator] 收到 Agent 原始输出，长度:", len(agent_raw_result))
        prompt = f"""
        请提取以下信息并转换为 JSON 数组格式。
        请严格按照以下 JSON 数组格式输出，不要包含任何 <think> 标签、Markdown 标记或解释性文字，只输出合法的 JSON：
        
        [
          {{
            "id": "item-1",
            "name": "中文名称",
            "severity": "Critical", 
            "score": 9.8, 
            "location": "路径或参数",
            "description": "详细的中文原理描述",
            "defense": "1. 中文建议一\\n2. 中文建议二" 
          }}
        ]
        
        【级别约束】：severity 字段必须严格使用以下四个单词之一：Low, Medium, High, Critical。
        如果没有发现任何有效项，请严格返回空数组 []。
        【严格警告】：你看到的日志包含了 Agent 自身的工具调用过程（如 launch_instance, navigate_to_url 等）。请绝对忽略这些本地工具的执行记录或报错，你只能提取目标网站（Target URL）本身存在的真实 Web 漏洞！
        原始信息：
        {agent_raw_result}
        """
        
        try:
            raw_response = self.llm.invoke(prompt).content
            print("[ReportGenerator] LLM 原始响应:\n" + raw_response[:500])
            json_str = self._extract_json(raw_response)
            print("[ReportGenerator] 提取的 JSON 字符串:", json_str[:500])
            result_json = json.loads(json_str)
            print(f"[ReportGenerator] ✅ JSON 解析成功，{len(result_json)} 条数据")
            return result_json
            
        except json.JSONDecodeError as e:
            print(f"[ReportGenerator] ❌ JSON 解析失败: {e}")
            print(f"[ReportGenerator] 尝试解析的字符串: {json_str[:500]}")
            return []
        except Exception as e:
            print(f"[ReportGenerator] ❌ 未知错误: {e}")
            import traceback
            traceback.print_exc()
            return []
