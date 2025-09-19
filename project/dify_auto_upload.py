import requests
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys

# === 配置区 ===
# 从环境变量中读取，如果不存在则使用默认值
API_KEY = os.getenv("API_KEY", "dataset-niArgvMgvqh8jCxPG9QsJv8A")
DATASET_ID = os.getenv("DATASET_ID", "f859dff0-28f3-455d-ac44-f71d3f49c1de")
WATCH_FOLDER = "upload_here"
PROCESS_RULE = '{"rules":{"split_by":"paragraph","chunk_size":500,"overlap_size":50}}'
DIFY_SERVER_URL = os.getenv("DIFY_SERVER_URL", "http://115.231.236.153:20000")

# 创建监控文件夹
os.makedirs(WATCH_FOLDER, exist_ok=True)

# 上传文件到 Dify 云端知识库
def upload_to_dify(file_path):
    url = f"{DIFY_SERVER_URL}/v1/datasets/{DATASET_ID}/document/create-by-file"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            data = {
                "name": os.path.basename(file_path),
                "process_rule": PROCESS_RULE
            }
            r = requests.post(url, headers=headers, files=files, data=data)

        if r.status_code in [200, 201]:
            print(f"[成功] {os.path.basename(file_path)} 已上传到 Dify 知识库。")
        else:
            print(f"[失败] {os.path.basename(file_path)} 上传失败：{r.status_code} {r.text}")

    except Exception as e:
        print(f"[错误] 上传文件 {file_path} 时出错：{e}")

# 文件夹监控
class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1) # 确保文件完全写入
            upload_to_dify(event.src_path)

if __name__ == "__main__":
    path = WATCH_FOLDER
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    print(f"开始监控文件夹：{WATCH_FOLDER}")
    print(f"目标Dify服务器：{DIFY_SERVER_URL}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()