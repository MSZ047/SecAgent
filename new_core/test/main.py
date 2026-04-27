from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import json
import os
from typing import Dict, Any

from app.models.schemas import ScanRequest, TaskStatus
from app.agents.vul_agent import run_vulnerability_scan
from app.tools.browser_tools import close_browser
from app.utils.report_generator import ReportGenerator

app = FastAPI(title="Vulnerability Audit Agent")

# [新增] 配置跨域，允许本地的前端 index.html 访问接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 任务状态存储
task_status: Dict[str, Dict[str, Any]] = {}
report_gen = ReportGenerator()  # [新增] 初始化翻译官

@app.post("/scan", response_model=TaskStatus)
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    task_status[task_id] = {
        "task_id": task_id,
        "status": "started",
        "progress": 0,
        "result": None,
        "error": None
    }
    
    # 丢入后台线程执行
    background_tasks.add_task(execute_scan_task, task_id, request)
    return TaskStatus(**task_status[task_id])

async def execute_scan_task(task_id: str, request: ScanRequest):
    try:
        task_status[task_id]["status"] = "running"
        task_status[task_id]["progress"] = 10

        print(f"[{task_id}] 🤖 Agent 开始扫描: {request.target_url}")
        raw_result = await run_vulnerability_scan(
            target_url=request.target_url,
            api_doc_url=getattr(request, 'api_doc_url', None),
            attacker_token=getattr(request, 'attacker_token', None),
            victim_user_id=getattr(request, 'victim_user_id', None)
        )
        task_status[task_id]["progress"] = 80

        print(f"[{task_id}] 📊 Agent 扫描完毕，正在生成可视化 JSON 数据...")
        agent_text = str(raw_result)
        print(f"\n--- Agent 原始输出开始 ---\n{agent_text}\n--- Agent 原始输出结束 ---\n")
        final_json = report_gen.generate_frontend_json(agent_text, request.target_url)

        task_status[task_id]["result"] = final_json
        task_status[task_id]["status"] = "completed"
        task_status[task_id]["progress"] = 100
        print(f"[{task_id}] ✅ 任务全流程完成！")

    except Exception as e:
        task_status[task_id]["status"] = "failed"
        task_status[task_id]["error"] = str(e)
        task_status[task_id]["progress"] = 100
        print(f"[{task_id}] ❌ 任务失败: {e}")
    finally:
        close_browser()

@app.get("/scan/{task_id}", response_model=TaskStatus)
async def get_scan_status(task_id: str):
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatus(**task_status[task_id])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)