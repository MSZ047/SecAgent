import json
from pathlib import Path
"""
本工具用来解决一些导入的新知识界面没有更新的问题
"""
def merge_historical_duplicates(wiki_dir: str = "./llmwiki", suffix: str = "_payload"):
    wiki_path = Path(wiki_dir)
    dirty_pages = []
    
    # 1. 找出所有带有特定后缀（如你截图中的 payload 后缀）的文件
    for file_path in wiki_path.glob(f"*{suffix}.md"):
        # 提取主干名称，比如从 "概念A_payload.md" 提取出 "概念A.md"
        main_name = file_path.name.replace(suffix, "")
        main_file_path = wiki_path / main_name
        
        print(f"发现重复对: {main_name} 和 {file_path.name}")
        
        # 2. 如果主文件存在，就把后缀文件的内容硬塞进去
        if main_file_path.exists():
            suffix_content = file_path.read_text(encoding="utf-8")
            main_content = main_file_path.read_text(encoding="utf-8")
            
            # 暴力追加
            main_file_path.write_text(main_content + f"\n\n### 从 {file_path.name} 合并的历史内容\n" + suffix_content, encoding="utf-8")
            
            # 3. 记录主文件为“脏页面”，交给后续的图书管理员去精简
            dirty_pages.append(main_name)
            
            # 4. 删除那个多余的后缀文件
            file_path.unlink()
            print(f"已合并并删除: {file_path.name}")

    # 5. 把所有合并过的主文件写入 dirty_pages.json
    if dirty_pages:
        state_file = wiki_path / "dirty_pages.json"
        existing = []
        if state_file.exists():
            existing = json.loads(state_file.read_text(encoding="utf-8"))
            
        updated_state = list(set(existing + dirty_pages))
        state_file.write_text(json.dumps(updated_state), encoding="utf-8")
        print(f"\n✅ 历史文件合并完毕！已将 {len(dirty_pages)} 个页面推入图书管理员的任务队列。")

if __name__ == "__main__":
    # 这里的 suffix 请替换为你实际想要合并清理的文件名后缀特征
    merge_historical_duplicates(suffix="_payload")