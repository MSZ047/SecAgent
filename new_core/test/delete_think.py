import re
from pathlib import Path

dir_path = Path("./llmwiki")
for path in dir_path.glob("*.md"):
    raw = path.read_text(encoding="utf-8")
    clean_text = re.sub(r'<think>.*?</think>', '', raw,flags=re.DOTALL).strip()
    if raw != clean_text:
        path.write_text(clean_text,encoding="utf-8")
        print(f"已成功清除{path}的页面")



