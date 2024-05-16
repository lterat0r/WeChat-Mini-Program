# coding:utf-8
import json
import time as t
from flask import Flask, render_template, request,jsonify
from werkzeug.utils import secure_filename
import cv2 as cv
import numpy as np
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

'''

配置上传目录，前端图片会上传到此目录下,
app.config['UPLOAD_FOLDER'] = 'upload/'

templates目录存放html文件

static目录存放html文件渲染的图片资源等，此目录下资源可通过url直接访问得到（如：http://192.168.3.7:5000/static/3.jpg)

logs输出日志



'''


UPLOADED_PHOTOS_DEST = './images/'  # 相对路径下的文件夹images
# UPLOADED_PHOTO_ALLOW = IMAGES		# 限制只能够上传图片

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/tupian/'





plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

path = r"D:/flask/upload/tupian"

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        img = cv.imread(event.src_path)
        # 灰度图转化
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        img1 = gray
        # 全局二值化
        ret, binary = cv.threshold(img1, 0, 255,
                                   cv.THRESH_BINARY | cv.THRESH_TRIANGLE)  # THRESH_OTSU自动阈值  方法不一样，阈值不一样（很有用，自己查！！！）
        # binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
        # ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
        img2 = binary
        # 图像反色
        img3 = cv.bitwise_not(img1)
        # 图像相乘
        img4 = cv.multiply(img3, img2)
        # 中值模糊  对椒盐噪声有很好的去燥效果
        img5 = cv.medianBlur(img4, 9)
        # 开闭运算去除不必要部分
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
        mb = cv.morphologyEx(img5, cv.MORPH_OPEN, kernel, iterations=2)
        img6 = cv.morphologyEx(mb, cv.MORPH_CLOSE, kernel, iterations=1)
        # 取反色
        img7 = cv.bitwise_not(img6)
        # 图像相加
        img8 = cv.add(img1, img7)
        # 取反色
        img9 = cv.bitwise_not(img8)
        # 相除
        img10 = cv.subtract(img6, img9)
        # rgb格式转化
        img11 = cv.cvtColor(img10, cv.COLOR_RGB2RGBA)
        cv.imwrite("img13.jpg", img11)
        img13 = cv.imread('img13.jpg')
        blurred = cv.pyrMeanShiftFiltering(img13, 5, 10)  # 去除噪点
        # 灰度
        img12 = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
        # 二值化
        ret1, thresh = cv.threshold(img12, 140, 255, cv.THRESH_BINARY)  # 118   125
        kerne1 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 形状 结构元素5*5
        # 腐蚀
        dst1 = cv.erode(thresh, kerne1)
        # 膨胀
        dst2 = cv.dilate(dst1, kernel)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 返回指定的形状和元素 椭圆形
        open = cv.morphologyEx(dst2, cv.MORPH_OPEN, kernel, iterations=2)  # 形态学开操作
        # 膨胀# 对“开运算”的结果进行膨胀，得到大部分都是背景的区域
        sure_bg = cv.dilate(open, kernel, iterations=1)
        dist_tran = cv.distanceTransform(sure_bg, cv.DIST_L2, 3)  # 距离变换
        dist_output = cv.normalize(dist_tran, 0, 1.0, cv.NORM_MINMAX)  # 归一化在0~1之间
        # 前景获取：种子区域

        # ret1, surface = cv.threshold(dist_tran, 0.2*dist_tran.max(), 255, cv.THRESH_BINARY)
        ret1, surface = cv.threshold(dist_output, dist_output.max() * 0.21, 255, cv.THRESH_BINARY)  # 0.68 3
        # ret1, surface = cv.threshold(dist_tran, dist_tran.max() * 0.6, 255, 0)
        surface_fg = np.uint8(surface)
        # 未知区域：#除种子以外的区域
        unknown = cv.subtract(sure_bg, surface_fg)
        # 标记
        ret1, markers = cv.connectedComponents(
            surface_fg)  # 连通区域# ret: 计算最大连通域  连通域：是由具有相同像素值的相邻像素组成像素集合# makers：将图像的背景标记为0
        #print(ret1)
        markers = markers + 1  # OpenCV 分水岭算法对物体做的标注必须都 大于1 ，背景为标号 为0  因此对所有markers 加1  变成了  1  -  N
        # 去掉属于背景区域的部分（即让其变为0，成为背景）
        # 此语句的Python语法 类似于if ，“unknow==255” 返回的是图像矩阵的真值表。
        markers[unknown == 255] = 0
        # Step8.分水岭算法
        markers = cv.watershed(img13, markers)  # 分水岭算法后，所有轮廓的像素点被标注为  -1
        #print(markers)
        img13[markers == -1] = [153, 51, 225]  # 标注为-1 的像素点标
        path2 = 'D:/flask/upload/tpchucun'
        cv.imwrite(os.path.join(path2, 'result.jpg'), img13)
        # cv.imshow('markeers',np.abs(markers))

        plt.imsave("biaoji.jpg", markers)
        img14 = cv.imread('biaoji.jpg')

        img15 = img14.copy()
        # img3 = np.zeros((img1.shape), dtype=np.uint8)
        # cv2.imwrite("C:/Users/Administrator/Desktop/2/3.jpg", img3)
        img16 = cv.addWeighted(img15, 0.4, img13, 0.7, 1)

        # 轮廓检测函数
        contours, hierarchy = cv.findContours(surface_fg, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        # 绘制轮廓
        cv.drawContours(surface_fg, contours, -1, (120, 0, 0), 2)

        count = 0  # 图像个数
        # 遍历找到的所有图像
        for cont in contours:
            # 计算包围性状的面积
            ares = cv.contourArea(cont)
            mj = ares * 6.4516 * 4 / 10 / 5184
            # 过滤面积小于30的形状
            if ares < 40:
                continue
            count += 1
            # 打印出每个图像的面积 体积
            # print("{}面积:{}".format(count, ares), end="  ")

            print("{}体积:{}".format(count, mj))

            # 提取矩形坐标（x,y）
            rect = cv.boundingRect(cont)
            # 打印坐标
            # print("x:{} y:{}".format(rect[0], rect[1]))
            # 绘制矩形 进行定位图像
            cv.rectangle(img16, rect, (0, 0, 120), 0)

            # 防止编号到图片之外（上面）,因为绘制编号写在左上角，所以让最上面的图像的y小于10的变为10个像素
            y = 10 if rect[1] < 10 else rect[1]
            # 在图像左上角写上编号
            cv.putText(img16, str(count), (rect[0], y), cv.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)
            # print('编号坐标：',rect[0],' ', y)

        #print('可疑区域个数', count)
        path1 = 'D:/flask/upload/tpchucun'
        cv.imwrite(os.path.join(path1,'imgshow.jpg'),img16)


    def on_deleted(self, event):
        if event.is_directory:
            print()
            #print("directory deleted:{0}".format(event.src_path))
        else:
            print()
            #print("file deleted:{0}".format(event.src_path))



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


@app.route("/uploader", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        start_time = t.time()
        f = request.files['file']
        if f is None:
            return "图片上传失败(failed)"
        global file_path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        end_time = t.time()
        used_time = end_time - start_time
        print(file_path + '图片用时%.3f s上传成功(file upload successfully)' % used_time)

        data = {
            "code": 200,
            "msg": "success"
        }
        return json.dumps(data)
    else:
        data = {
            "code": 405,
            "msg": "Method Not Allowed"
        }
        return json.dumps(data)
        ################  do something  图像处理啥的   ################



# 启动路由,访问http://192.168.3.7:5000
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)