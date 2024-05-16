import requests
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

path = r"D:/flask/upload/tpchucun"
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        upload_url = "http://127.0.0.1:5000/uploader/transmission"
        # 上传文件的信息头
        upload_header = {"token":"0xFFD8FF"}
        # 上传文件(图片)的请求参数
        file = {"file": open(r"D:/flask/15.jpg", "rb")}
        # 发送请求 ---> 注意别写错了，是files
        upload_res = requests.post(url=upload_url,files=file,headers=upload_header)
        print(upload_res.json())


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


