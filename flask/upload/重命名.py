
import os
import shutil
import datetime
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


path = r"D:\flask\tpchulijieguo"
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  # 现在
        dir = r'D:\flask\tpchulijieguo'
        for root, dirs, file in os.walk(dir):
            for b in file:
                if os.path.join(b).split('.')[1] == 'jpg':
                # os.rename(dir + os.sep + b, dir + os.sep + str(nowTime) + '_' + b)
                    shutil.copy(os.path.join(dir, b), os.path.join(r'D:\flask\tupianchuli', str(nowTime) + '_' + b))
                # shutil.copy(os.path.join(dir, str(nowTime) + '_' + b), r'/home/kangle/result')


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