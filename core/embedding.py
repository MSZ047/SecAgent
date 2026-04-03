import lancedb
import ollama
import os
from docx import Document
from pathlib import Path
# rag的使用方法，先把文档放在word文件夹下面，接着运行rag这个文件
# 就会自动向量化

BASE_DIR = Path(__file__).resolve().parent # rag转到core
MODEL_NAME = "nomic-embed-text" 
DB_PATH = BASE_DIR / "security"
DONE_FOLDER = BASE_DIR / "word" / "done" # core转到word/done
TABLE_NAME =  "vul_doc"
RAW_FOLDER = BASE_DIR / "word" / "raw"
def read_file(file_path):
    tmp=[]
    doc = Document(file_path)
    for p in doc.paragraphs:
        if p.text.strip():
            tmp.append(p.text)
    return "\n".join(tmp)

db = lancedb.connect(DB_PATH)

# def create_chunk():
    
    
def embedding():
    if not os.path.exists(DONE_FOLDER):
        print("先创建文件夹")
    else:
        data = []
        for file in os.listdir(DONE_FOLDER):
            try:
                if file.endswith("docx"):# 确定的是docx文档
                    print("正在处理文件")
                    
                    # 获取文件的完整路径
                    full_path = DONE_FOLDER / file 
                    
                    # 获取文件内容
                    raw_text  = read_file(full_path) 
                    
                    #向量化
                    response = ollama.embeddings(model=MODEL_NAME, prompt=raw_text)
                    
                    # 取出embedding部分的内容
                    vector = response["embedding"]
                    
                    # 添加进data临时列表
                    data.append({
                        "vector":vector,
                        "raw":raw_text,
                        "file_name":file}
                        )
            except Exception as e:
                print(f"处理文件{file}时候出错：{e}")
        #写入数据库
        if data :
            #添加数据进入表内
            if TABLE_NAME in db.list_tables():
                table = db.open_table(TABLE_NAME)  
                table.add(data) 
            #没有表创建
            else: 
                table = db.create_table(TABLE_NAME,data)
        else:
            print("文档没加载进来")
#程序入口时embedding
if __name__ == "__main__":
    embedding()               
        