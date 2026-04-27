# test_async.py
import asyncio
from app.tools.browser_tools import navigate_to_url, get_snapshot_interactive, execute_action

async def main():
    print(await navigate_to_url.ainvoke({"url": "http://httpbin.org/forms/post"}))
    print(await get_snapshot_interactive.ainvoke({}))
    print(await execute_action.ainvoke({"action": "fill", "element_id": "e0", "value": "test"}))

asyncio.run(main())