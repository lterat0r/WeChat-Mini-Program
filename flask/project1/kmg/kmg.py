import time
import os
import shutil
import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import cv2 as cv
import numpy as np
from skimage import morphology
import tkinter as tk
from tkinter import filedialog
from skimage.measure import label
import matplotlib.pyplot as plt
from skimage import io, transform, img_as_float
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

path = r"D:/flask/upload/tupian"
# 自定义处理类
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        import os
        os.popen('python f2.py') #可疑持续搞图像

        #os.system('python f2.py')  #进行一遍输出

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



