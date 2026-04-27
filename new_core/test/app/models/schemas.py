from pydantic import BaseModel
from typing import Any,List, Optional

class ScanRequest(BaseModel):
    target_url: str
    api_doc_url: Optional[str] = None
    extra_files: List[str] = []
    attacker_token: Optional[str] = None
    victim_user_id: Optional[str] = None

class Vulnerability(BaseModel):
    type: str
    severity: float
    location: str
    proof_of_concept: str
    recommendation: str

class ScanResult(BaseModel):
    target_url: str
    vulnerabilities_found: List[Vulnerability]
    test_summary: dict

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: int
    # 【核心修复】把 dict 改成 Any，允许我们存放 JSON 列表
    result: Optional[Any] = None 
    error: Optional[str] = None