from pathlib import Path
from app.utils.llmwiki import LLMWikiManager
import os

# ================= 各种解析引擎加载 =================

# 1. 加载 OCR 引擎 (处理图片)
try:
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    OCR_AVAILABLE = True
except ImportError:
    print("⚠️ 警告: 未安装 rapidocr_onnxruntime，图片读取功能将被禁用。")
    OCR_AVAILABLE = False

# 2. 加载 DOCX 引擎 (处理 Word)
try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    print("⚠️ 警告: 未安装 python-docx，.docx 文件读取功能将被禁用。")
    DOCX_AVAILABLE = False


# ================= 提取逻辑 =================

def extract_text_from_image(image_path: str) -> str:
    """使用 RapidOCR 从图片中提取文本"""
    if not OCR_AVAILABLE:
        return "[图片内容无法读取：OCR模块未安装]"
    
    result, _ = ocr(image_path)
    if result:
        extracted_text = "\n".join([line[1] for line in result])
        return extracted_text
    return "[图片中未识别到文本]"

def extract_text_from_docx(file_path: str) -> str:
    """使用 python-docx 提取 Word 文档中的所有文本"""
    if not DOCX_AVAILABLE:
        return "[.docx内容无法读取：python-docx模块未安装]"
    
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():  # 只保留非空段落
                full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return f"[读取.docx失败: {str(e)}]"

# ================= 核心消化系统 =================

def ingest_local_directory(source_dir: str):
    wiki_manager = LLMWikiManager()
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"❌ 找不到目录: {source_dir}，请先创建它！")
        return
        
    print(f"🚀 开始扫描目录: {source_dir} ...\n")
    
    # 扩展支持的文件类型
    text_extensions = ['.txt', '.md', '.json', '.log', '.csv']
    image_extensions = ['.png', '.jpg', '.jpeg']
    docx_extensions = ['.docx']
    
    success_count = 0
    for file_path in source_path.rglob("*"):
        if not file_path.is_file():
            continue
            
        ext = file_path.suffix.lower()
        raw_content = ""
        
        try:
            # 分支 1：处理纯文本
            if ext in text_extensions:
                print(f"📖 正在阅读文本文件: {file_path.name} ...")
                raw_content = file_path.read_text(encoding="utf-8")
                
            # 分支 2：处理图片 (OCR)
            elif ext in image_extensions:
                print(f"👁️ 正在对图片进行 OCR 识别: {file_path.name} ...")
                raw_content = extract_text_from_image(str(file_path))
                if not raw_content.strip():
                    print(f"   ⚠️ 跳过，图片中无有效文本。")
                    continue
                    
            # 分支 3：处理 Word 文档
            elif ext in docx_extensions:
                print(f"📄 正在解析 Word 文档: {file_path.name} ...")
                raw_content = extract_text_from_docx(str(file_path))
                if not raw_content.strip():
                    print(f"   ⚠️ 跳过，文档为空或提取失败。")
                    continue
                    
            # 其他格式直接忽略
            else:
                continue 
                
            # 🎯 【核心修改点】调用全新的 ingest 方法，不再接收单一文件名
            print(f"   🧠 正在让 LLM 思考如何将此文档融入维基知识库，请稍候...")
            wiki_manager.ingest(
                raw_content=raw_content,
                source_url=f"本地导入: {file_path.name}"
            )
            
            print(f"   ✅ {file_path.name} 摄取完毕！")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ 处理文件 {file_path.name} 时出错: {str(e)}")
                
    print(f"\n🎉 批量摄取完成！共成功处理 {success_count} 份源文档。")
    print(f"👉 快去看看 llmwiki 目录下的 index.md 和 log.md 发生了什么变化吧！")

if __name__ == "__main__":
    TARGET_DIR = "./raw_docs"
    ingest_local_directory(TARGET_DIR)