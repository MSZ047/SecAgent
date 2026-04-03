from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from pathlib import Path
import lancedb
import ollama

# 连接数据库
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "security"
security = lancedb.connect(str(DB_PATH))
@tool # langchain底层的说明书生成器，把docstring和函数名称之类的提炼发给模型
      # 类似于c语言的头文件
def search_vul_base(query:str) -> str:
    """
    搜索本地网络安全知识库。
    当你遇到不确定的漏洞特征、或者需要查阅修复建议时，必须优先调用此工具。
    输入参数应该是一个明确的搜索短语，例如 "SQL注入修复建议"。
    """
    print(f"\n[工具被调用] SecAgent 正在搜索知识库: {query}")
    
    print("[调试] 正在调用 nomic 算向量...")
    response = ollama.embeddings(model="nomic-embed-text", prompt=query)
    query_vector = response["embedding"]
    print("[调试] 向量计算完成！")
    
    print("[调试] 正在搜索 LanceDB...")
    table = security.open_table("vul_doc") 
    result = table.search(query_vector).limit(2).to_pandas()
    print(f"[调试] 数据库搜索完成，找到 {len(result)} 条结果！")
    
    final_text = ""
    for index, row in result.iterrows():
        # 给提取的内容加个长度限制，防止大模型被撑死 (截取前500字符)
        content = str(row['raw'])[:500] 
        final_text += f"来源文件：{row['file_name']}\n内容:{content}...\n\n"
        
    print(f"⏳ [调试] 工具执行完毕，准备把 {len(final_text)} 个字符返回给 Qwen，请等待模型思考...")
    return final_text

# 选择对应的模型，并告诉模型可以使用的工具，以及系统提示词
qwen = ChatOllama(model="qwen2.5:latest",temperature=1)
tools = [search_vul_base]
system_prompt = """
你是一个顶级的网络安全专家。
你的任务是分析用户提供的 HTTP 报文或代码片段，判断是否存在漏洞。
如果遇到不确定的漏洞细节，请务必使用工具搜索本地知识库。
请用专业、客观的语气输出分析报告，包含：1. 漏洞确认 2. 危险等级 3. 修复建议。
"""

# qwen_with_tools = qwen.bind_tools(tools)# 这里的tools是给模型层看的，像当于给模型的说明书
# prompt = ChatPromptTemplate.from_messages([ # 注意这里的括号要紧贴from_message，在py中函数名和括号不能换行
#     ("system", """你是一个顶级的网络安全专家。
# 你的任务是分析用户提供的 HTTP 报文或代码片段，判断是否存在漏洞。
# 如果遇到不确定的漏洞细节，请务必使用工具搜索本地知识库。
# 请用专业、客观的语气输出分析报告，包含：1. 漏洞确认 2. 危险等级 3. 修复建议。"""),
#     ("placeholder", "{chat_history}"),# 大括号里面的是占位符，相当于c语言里面的%c
#     ("human", "{input}"),
#     ("placeholder", "{agent_scratchpad}"), # 这是给 Agent 思考和记录工具返回结果用的“草稿纸”
# ])


# 组装运行
def SecAgent_up(target_data: str):
    print("启动SecAgent（langGraph版）")
    # 使用最新的引擎
    agent_executor = create_agent(
        model=qwen,
        tools=tools,
        system_prompt=system_prompt
        )
    # 用 f-string 把用户的纯报文包装成一段明确的命令
    wrapped_prompt = f"请帮我严格分析下面这段 HTTP 报文是否存在漏洞。如果不确定特征或修复方案，请务必调用搜索工具查阅知识库！\n\n【待分析报文如下】：\n{target_data}"
    
    result = agent_executor.invoke({"messages": [HumanMessage(content=wrapped_prompt)]})
    # # 创建agent
    # agent = create_tool_calling_agent(qwen,tools,prompt) # 这里的tools是给langchain逻辑层看的，让逻辑层判断白名单
    # # 创建执行器（把agent和tools绑定在一起，开启verbose=true看思考过程）
    # agent_executer = AgentExecutor(agent=agent,tools=tools,verbose=True)# 这里的tools是给执行层看的，实际执行代码的
    #                                                                     # 这三个tools共同组成了langchain的调用逻辑 
    # # 执行分析任务
    # result = agent_executer.invoke({"input": target_data})
    print("\n" + "#"*50)
    print("最终分析报告")
    print(result["messages"][-1].content)
    print("#"*50)
    
if __name__ == "__main__":# 函数入口
    # data=input("请输入想要分析的内容")
    # SecAgent_up(data)
    sample_http_data = """
    POST /login.php HTTP/1.1
    Host: example.com
    Content-Type: application/x-www-form-urlencoded
    
    username=admin' OR '1'='1&password=123
    """
    
    SecAgent_up(sample_http_data) 
    
    
    
    
    