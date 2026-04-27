import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from app.tools.browser_tools import navigate_to_url, get_snapshot_interactive, get_page_text, execute_action
from app.tools.knowledge_tools import read_wiki, submit_to_wiki
from app.config.settings import settings

def create_vulnerability_agent():
    llm = ChatOpenAI(
        model="MiniMax-M2",
        api_key=settings.minimax_api_key,
        base_url="https://api.minimaxi.com/v1",
        temperature=0.7
    )
    tools = [
        navigate_to_url, get_snapshot_interactive, get_page_text,
        execute_action, read_wiki, submit_to_wiki
    ]
    agent_executor = create_react_agent(model=llm, tools=tools)
    return agent_executor

async def run_vulnerability_scan(target_url: str, api_doc_url: str = None,
                                 attacker_token: str = None, victim_user_id: str = None):
    agent = create_vulnerability_agent()

    with open("app/agents/sys_prompt.txt", "r", encoding="utf-8") as f:
        system_message = f.read()

    scan_prompt = f"""
    对网站 {target_url} 进行分析。
    如有 API 文档 URL: {api_doc_url}
    """

    result = await agent.ainvoke({
        "messages": [
            ("system", system_message),
            ("user", scan_prompt)
        ]
    })

    final_output = result["messages"][-1].content
    return final_output