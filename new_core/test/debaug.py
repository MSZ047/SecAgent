# debug_snapshot.py
import sys
sys.path.insert(0, '.')  # 确保能找到 app 模块

from app.tools.browser_tools import navigate_to_url, get_snapshot_interactive

# 先用 Agent 同样的目标 URL
print(navigate_to_url.invoke({"url": "http://hq4zqkb.haobachang1.loveli.com.cn:8888"}))
print("=" * 40)
print("页面内容（HTML 前 2000 字符）：")
# 这里我们不能直接调 Playwright 的 page 对象，所以换个方式：
# 在 browser_tools.py 里临时加上一个导出 _page 的变量，或者直接在这个脚本里复制 _ensure_page