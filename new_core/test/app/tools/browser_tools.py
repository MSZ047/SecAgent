from langchain.tools import tool
from playwright.sync_api import sync_playwright

_playwright = None
_browser = None
_page = None


def _ensure_page():
    global _playwright, _browser, _page
    if _page is None:
        _playwright = sync_playwright().start()
        _browser = _playwright.chromium.launch(headless=True)
        _page = _browser.new_page()
    return _page


def close_browser():
    global _playwright, _browser, _page
    try:
        if _page:
            _page.close()
            _page = None
        if _browser:
            _browser.close()
            _browser = None
        if _playwright:
            _playwright.stop()
            _playwright = None
    except Exception:
        pass


@tool("navigate_to_url")
def navigate_to_url(url: str) -> str:
    """跳转到指定 URL"""
    print("模型调用跳转到url函数\n")
    try:
        page = _ensure_page()
        page.goto(url, timeout=15000)
        return f"Navigated to {url}"
    except Exception as e:
        return f"Navigation error: {str(e)}"


@tool("get_snapshot_interactive")
def get_snapshot_interactive() -> str:
    """获取可交互元素列表（精简 JSON）。包含元素 ID(e0,e1...) 供 execute_action 使用。"""
    print("模型调用获取浏览器内容的函数\n")
    try:
        page = _ensure_page()
        title = page.title()
        url = page.url
        print(f"[DEBUG] 当前页面: {url} | 标题: {title}")
        elements = page.evaluate("""() => {
            const items = [];
            const nodes = document.querySelectorAll('input, button, select, textarea, a, [onclick]');
            nodes.forEach((el, idx) => {
                items.push({
                    id: 'e' + idx,
                    tag: el.tagName,
                    type: el.type || '',
                    text: (el.innerText || el.value || el.placeholder || '').substring(0, 50),
                    idAttr: el.id,
                    name: el.name
                });
            });
            return JSON.stringify(items);
        }""")
        print(f"[SNAPSHOT] {elements}")
        return elements
    except Exception as e:
        return f"Snapshot error: {str(e)}"


@tool("get_page_text")
def get_page_text() -> str:
    """获取页面 body 内的全部可见文本（用于判断攻击结果）。每次 execute_action 后必须调用此工具查看页面反馈。"""
    print("模型调用获取页面文本函数\n")
    try:
        page = _ensure_page()
        text = page.evaluate("() => (document.body ? document.body.innerText : '') || ''")
        text = text[:3000]
        print(f"[PAGE_TEXT] 前200字符: {text[:200]}")
        return text
    except Exception as e:
        return f"Page text error: {str(e)}"


@tool("execute_action")
def execute_action(action: str, element_id: str, value: str = None) -> str:
    """执行动作，element_id 为快照中的 e0, e1... 支持 action: click/fill/press"""
    print("模型开始调用执行函数\n")
    try:
        page = _ensure_page()
        idx = int(''.join(c for c in element_id if c.isdigit()))
        selector = 'input, button, select, textarea, a, [onclick]'
        el = page.locator(selector).nth(idx)
        if action == 'click':
            el.click(timeout=10000)
        elif action == 'fill':
            el.fill(value or '', timeout=10000)
        elif action == 'press':
            el.press(value or 'Enter', timeout=10000)
        page.wait_for_load_state('networkidle', timeout=10000)
        return f"Action {action} on {element_id} done"
    except Exception as e:
        return f"Action error: {str(e)}"
