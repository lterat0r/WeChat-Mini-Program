import time

from flask import Flask
from flask_caching import Cache
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import cv2 as cv
import numpy as np
import os
import json
#from skimage import morphology
import tkinter as tk
from tkinter import filedialog
#from skimage.measure import label
import matplotlib.pyplot as plt
#from skimage import io, transform, img_as_float
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

path = r"C:/flask/upload/tupian1"

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 600,
    "CACHE_REDIS_HOST": "127.0.0.1",
    "CACHE_REDIS_PORT": '6379',
    "CACHE_REDIS_DB": 0,
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

# 自定义处理类
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        img02 = cv.imread(event.src_path)
        img999 = cv.imread('C:/jh/01/9999.png')
        img2 = img02
        imgq1 = cv.resize(img2, (921, 1440))
        print(img2.shape)
        print(imgq1.shape)

        # img1=cv.imread("C:/Users/Administrator/Desktop/xxy/9999.png")
        # img2=cv.imread("C:/Users/Administrator/Desktop/xxy/01.png")
        img3 = cv.add(img999, imgq1)
        cv.imshow("diejia", img3)
        # cv.imwrite("diejia.png",img3)

        # img3 = img3[136:289, 779:932]  # x0,y0为裁剪区域左上坐标；x1,y1为裁剪区域右下坐标
        cv.imwrite('diejia1.png', img3)
        cv.imshow('55', img3)

        img = cv.imread('diejia1.png')  # img_path为图片所在路径
        img3 = img[289:932, 136:779]  # x0,y0为裁剪区域左上坐标；x1,y1为裁剪区域右下坐标
        cv.imwrite("diejia.png", img3)  # save_path为保存路径

















        def resizeImg(image, height=900):
            h, w = image.shape[:2]
            pro = height / h
            size = (int(w * pro), int(height))
            img = cv.resize(image, size)
            return img

        # 边缘检测
        def getCanny(image):
            # 高斯模糊
            binary = cv.GaussianBlur(image, (3, 3), 1, 1)
            # 边缘检测
            binary = cv.Canny(binary, 60, 240, apertureSize=3)
            # 膨胀操作，尽量使边缘闭合
            kernel = np.ones((3, 3), np.uint8)
            binary = cv.dilate(binary, kernel, iterations=1)
            return binary

        global path
        path = r'diejia.png'
        outpath = r'getCanny.jpg'
        img = cv.imread(path)
        img = resizeImg(img)
        print('shape =', img.shape)
        binary_img = getCanny(img)
        cv.imwrite(outpath, binary_img)

        # output:    shape = (900, 420, 3)
        # 代码承接上文
        # 求出面积最大的轮廓
        def findMaxContour(image):
            # 寻找边缘
            contours, hierarchy = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
            # 计算面积
            max_area = 0.0
            max_contour = []
            for contour in contours:
                currentArea = cv.contourArea(contour)
                if currentArea > max_area:
                    max_area = currentArea
                    max_contour = contour
            return max_contour, max_area

        outpath = r'findMaxContour.jpg'
        img = cv.imread(path)
        img = resizeImg(img)
        binary_img = getCanny(img)
        max_contour, max_area = findMaxContour(binary_img)
        cv.drawContours(img, max_contour, -1, (0, 0, 255), 3)
        cv.imwrite(outpath, img)

        # 代码承接上文
        # 多边形拟合凸包的四个顶点
        def getBoxPoint(contour):
            # 多边形拟合凸包
            hull = cv.convexHull(contour)
            epsilon = 0.001 * cv.arcLength(contour, True)
            approx = cv.approxPolyDP(hull, epsilon, True)
            approx = approx.reshape((len(approx), 2))
            return approx

        outpath = r'getBoxPoint.jpg'
        img = cv.imread(path)
        img = resizeImg(img)
        binary_img = getCanny(img)
        max_contour, max_area = findMaxContour(binary_img)
        boxes = getBoxPoint(max_contour)
        for box in boxes:
            cv.circle(img, tuple(box), 5, (0, 0, 255), 2)
        print(boxes)
        cv.imwrite(outpath, img)

        # 代码承接上文
        # 适配原四边形点集
        def adaPoint(box, pro):
            box_pro = box
            if pro != 1.0:
                box_pro = box / pro
            box_pro = np.trunc(box_pro)
            return box_pro

        # 四边形顶点排序，[top-left, top-right, bottom-right, bottom-left]
        def orderPoints(pts):
            rect = np.zeros((4, 2), dtype="float32")
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]
            return rect

        # 计算长宽
        def pointDistance(a, b):
            return int(np.sqrt(np.sum(np.square(a - b))))

        # 透视变换
        def warpImage(image, box):
            w, h = pointDistance(box[0], box[1]), \
                   pointDistance(box[1], box[2])
            dst_rect = np.array([[0, 0],
                                 [w - 1, 0],
                                 [w - 1, h - 1],
                                 [0, h - 1]], dtype='float32')
            M = cv.getPerspectiveTransform(box, dst_rect)
            warped = cv.warpPerspective(image, M, (w, h))
            return warped

        outpath = r'result.jpg'
        image = cv.imread(path)
        ratio = 900 / image.shape[0]
        img = resizeImg(image)
        binary_img = getCanny(img)
        max_contour, max_area = findMaxContour(binary_img)
        boxes = getBoxPoint(max_contour)
        boxes = adaPoint(boxes, ratio)
        boxes = orderPoints(boxes)
        # 透视变化
        warped = warpImage(image, boxes)
        cv.imwrite(outpath, warped)

        img = cv.imread('result.jpg')
        cv.imshow("0", img)
        print(img.shape)
        blurred = cv.pyrMeanShiftFiltering(img, 10, 10)  # 去除噪点
        # 中值模糊  对椒盐噪声有很好的去燥效果

        # 灰度图转化
        gray = cv.cvtColor(blurred, cv.COLOR_RGB2GRAY)
        cv.imshow("img1", gray)
        img1 = gray
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        mb = cv.morphologyEx(img1, cv.MORPH_OPEN, kernel, iterations=5)
        img6 = cv.morphologyEx(mb, cv.MORPH_CLOSE, kernel, iterations=3)

        # 全局二值化
        ret, binary = cv.threshold(img6, 198, 255, cv.THRESH_BINARY_INV)  # THRESH_OTSU自动阈值  方法不一样，阈值不一样（很有用，自己查！！！）
        # binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
        # ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
        print("threshold value %s" % ret)

        img2 = binary
        cv.imshow("img2", img2)

        # 图像反色
        img3 = cv.bitwise_not(img1)
        cv.imshow("img3", img3)

        # 图像相乘
        img4 = cv.multiply(img3, img2)
        cv.imshow("img4", img4)

        # 中值模糊  对椒盐噪声有很好的去燥效果
        img5 = cv.medianBlur(img4, 9)
        cv.imshow("img5", img5)

        # 开闭运算去除不必要部分
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        mb = cv.morphologyEx(img5, cv.MORPH_OPEN, kernel, iterations=3)
        img6 = cv.morphologyEx(mb, cv.MORPH_CLOSE, kernel, iterations=1)
        cv.imshow("img6", img6)

        # 取反色
        img7 = cv.bitwise_not(img6)
        cv.imshow("img7", img7)

        # 图像相加
        img8 = cv.add(img1, img7)
        cv.imshow("img8", img8)

        # 取反色
        img9 = cv.bitwise_not(img8)
        cv.imshow("img9", img9)

        # 相除
        img10 = cv.subtract(img6, img9)
        cv.imshow("img10", img10)

        # rgb格式转化
        img11 = cv.cvtColor(img10, cv.COLOR_RGB2RGBA)
        cv.imshow("img11", img11)
        cv.imwrite("img13.jpg", img11)
        img13 = cv.imread('img13.jpg')
        print(img13.shape)

        blurred = cv.pyrMeanShiftFiltering(img13, 5, 10)  # 去除噪点

        # 灰度
        img12 = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
        # 二值化

        ret1, thresh = cv.threshold(img12, 35, 255, cv.THRESH_BINARY_INV)  # 118   125
        cv.imshow("erzhihua", thresh)

        kerne1 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 形状 结构元素5*5
        # 腐蚀
        dst1 = cv.erode(thresh, kerne1)
        cv.imshow("erode_demo", dst1)

        # 膨胀
        dst2 = cv.dilate(dst1, kerne1)

        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 返回指定的形状和元素 椭圆形
        open = cv.morphologyEx(dst2, cv.MORPH_OPEN, kernel, iterations=2)  # 形态学开操作
        cv.imshow("open", open)

        # 膨胀# 对“开运算”的结果进行膨胀，得到大部分都是背景的区域
        sure_bg = cv.dilate(open, kernel, iterations=1)
        cv.imshow("beijing", sure_bg)

        dist_tran = cv.distanceTransform(sure_bg, cv.DIST_L2, 3)  # 距离变换
        dist_output = cv.normalize(dist_tran, 0, 1.0, cv.NORM_MINMAX)  # 归一化在0~1之间
        cv.imshow("dist_output", dist_output * 70)
        cv.imshow("dist_tran", dist_tran * 70)

        # 前景获取：种子区域
        # ret1, surface = cv.threshold(dist_tran, 0.2*dist_tran.max(), 255, cv.THRESH_BINARY)
        ret1, surface = cv.threshold(dist_output, dist_output.max() * 0.2, 255, cv.THRESH_BINARY)  # 0.68 3
        # ret1, surface = cv.threshold(dist_tran, dist_tran.max() * 0.6, 255, 0)
        surface_fg = np.uint8(surface)
        cv.imshow("surface", surface_fg)

        # 未知区域：#除种子以外的区域
        unknown = cv.subtract(sure_bg, surface_fg)
        # 标记
        ret1, markers = cv.connectedComponents(
            surface_fg)  # 连通区域# ret: 计算最大连通域  连通域：是由具有相同像素值的相邻像素组成像素集合# makers：将图像的背景标记为0
        print(ret1)

        markers = markers + 1  # OpenCV 分水岭算法对物体做的标注必须都 大于1 ，背景为标号 为0  因此对所有markers 加1  变成了  1  -  N
        # 去掉属于背景区域的部分（即让其变为0，成为背景）
        # 此语句的Python语法 类似于if ，“unknow==255” 返回的是图像矩阵的真值表。
        markers[unknown == 255] = 0

        # Step8.分水岭算法
        markers = cv.watershed(img13, markers)  # 分水岭算法后，所有轮廓的像素点被标注为  -1
        print(markers)
        img13[markers == -1] = [153, 51, 225]  # 标注为-1 的像素点标
        # cv.imshow('markeers',np.abs(markers))
        cv.imshow('result', img13)

        plt.imsave("biaoji.jpg", markers)
        img14 = cv.imread('biaoji.jpg')

        img15 = img14.copy()
        # img3 = np.zeros((img1.shape), dtype=np.uint8)
        # cv.imwrite("C:/Users/Administrator/Desktop/2/3.jpg", img3)
        img16 = cv.addWeighted(img15, 0.4, img13, 0.7, 1)
        cv.imshow("diejia", img16)

        path10 = r'C:/flask/tpchulijieguo'
        cv.imwrite(os.path.join(path10, '111.jpg'), img16)
        # 轮廓检测函数
        contours, hierarchy = cv.findContours(surface_fg, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        # 绘制轮廓
        cv.drawContours(surface_fg, contours, -1, (120, 0, 0), 2)

        count = 0  # 图像个数
        mjList = []
        global res
        res = 0
        # 遍历找到的所有图像
        for cont in contours:
            # 计算包围性状的面积
            ares = cv.contourArea(cont)
            res = max(ares, res)
            mj = ares * 6.4516 * 4 / 10 / 5184
            a = round(mj, 2)
            # 过滤面积
            if ares < 50:
                continue
            count += 1
            # 打印出每个图像的面积 体积
            # print("{}面积:{}".format(count, ares), end="  ")
            print("{}体积:{}".format(count, mj))
            mjList.append({
                "count": count,
                "mj": mj
            })
            # 提取矩形坐标（x,y）
            rect = cv.boundingRect(cont)
            # 打印坐标
            # print("x:{} y:{}".format(rect[0], rect[1]))
            # 绘制矩形 进行定位图像
            cv.rectangle(img16, rect, (0, 0, 120), 0)

            # 防止编号到图片之外（上面）,因为绘制编号写在左上角，所以让最上面的图像的y小于10的变为10个像素
            y = 10 if rect[1] < 10 else rect[1]
            # 在图像左上角写上编号
            # 在图像左上角写上编号
            cv.putText(img16, 'qv{} tj:{}'.format(count, a), (rect[0], y), cv.FONT_HERSHEY_COMPLEX, 2, (15, 25, 0), 0)
            # print('编号坐标：',rect[0],' ', y)
            # print('编号坐标：',rect[0],' ', y)
            cv.imwrite("C:/flask/tpchulijieguo1/paizhaojieguo/jieguo.jpg",img16)

            # print("出血量:{}".format(res))
            check()
            # print('可疑区域',count)
            # cv.namedWindow("imagshow", 2)  # 创建一个窗口
            # cv.imshow('imagshow', img16)  # 显示原始图片（添加了外接矩形）

            cache_name = event.src_path
            result = eval(repr(cache_name).replace('\\', '/'))
            cache_name = result.replace("C:/flask/upload/tupian/", "")
            cache_name = cache_name.replace("/", "")
            arrname = cache_name.split('.')
            cache.set(arrname[0], json.dumps(mjList, ensure_ascii=False), 600)
            # filename = r'D:/flask/mj_json'
            # print(filename)
            path1 = r'C:/flask/tpchulijieguo1'
            cv.imwrite(os.path.join(path1, '111.jpg'), img16)
            # json_file = open(os.path.join(filename,arrname[0]+'.json'), 'w', encoding='utf-8')
            # json_file.write(json.dumps(mjList, ensure_ascii=False))
            # json_file.close()

        def on_deleted(self, event):
            if event.is_directory:
                print("directory deleted:{0}".format(event.src_path))
            else:
                print("file deleted:{0}".format(event.src_path))



# 创建一个txt文件，文件名为mytxtfile,并向文件写入msg
def text_create(name, msg):
    desktop_path = "C:/Users/Administrator/Desktop/"  # 新创建的txt文件的存放路径
    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w')
    file.write(msg)  # msg也就是下面的Hello world!
    # file.close()

def check():
    print("出血量:{}".format(res))
    # t = res
    # amount = 0
    # while t > 1:
    #     t /= 10
    #     amount += 1
    # print(amount)
    if res < 1000:
        text_create('mytxtfile2', '第一级')
    if res >= 1000 and res < 2000:
        text_create('mytxtfile2', '第二级')
    if res >= 2000 and res < 3000:
        text_create('mytxtfile2', '第三级')
    if res >= 3000 and res < 4000:
        text_create('mytxtfile2', '第四级')
    if res >= 4000 and res < 5000:
        text_create('mytxtfile2', '第五级')
    if res >= 5000:
        text_create('mytxtfile2', '第六级')
    # 属于百分之？
    # return print(方案1)

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
