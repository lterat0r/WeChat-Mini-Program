import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 自定义处理类
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("文件被修改了 %s"%event.src_path)


if __name__ == "__main__":
    path = "."
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
