import cv2
import numpy as np
import cv2 as cv
import numpy as np
import os
from skimage import morphology
import tkinter as tk
from tkinter import filedialog
from skimage.measure import label
import matplotlib.pyplot as plt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from skimage.io import ImageCollection
from skimage import io, transform, img_as_float
import time
import shutil

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

path = r'C:/flask/upload/cs4'


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global max_area

        img_path = r'C:/flask/upload/000'

        # global img
        RGA(img_path)
        global img1

        img1 = RGA(img_path)

        img_path1 = r'C:/flask/upload/cs3'

        RGA1(img_path1)

        img2 = RGA1(img_path1)
        imgq1 = cv2.resize(img2, (921, 1440))

        # img1=cv2.imread("C:/Users/Administrator/Desktop/xxy/9999.png")
        # img2=cv2.imread("C:/Users/Administrator/Desktop/xxy/01.png")
        img3 = cv2.add(img1, imgq1)
        # cv2.imwrite("diejia.png",img3)

        # img3 = img3[136:289, 779:932]  # x0,y0为裁剪区域左上坐标；x1,y1为裁剪区域右下坐标
        cv2.imwrite('diejia1.png', img3)

        img = cv2.imread('diejia1.png')  # img_path为图片所在路径
        img3 = img[289:932, 136:779]  # x0,y0为裁剪区域左上坐标；x1,y1为裁剪区域右下坐标
        cv2.imwrite("diejia.png", img3)  # save_path为保存路径

        global path
        path = r'diejia.png'
        outpath = r'getCanny.jpg'
        img = cv2.imread(path)
        img = resizeImg(img)
        print('shape =', img.shape)
        binary_img = getCanny(img)
        cv2.imwrite(outpath, binary_img)
        # output:    shape = (900, 420, 3)

        outpath = r'findMaxContour.jpg'
        img = cv2.imread(path)
        img = resizeImg(img)
        binary_img = getCanny(img)
        max_contour, max_area = findMaxContour(binary_img)
        cv2.drawContours(img, max_contour, -1, (0, 0, 255), 3)
        cv2.imwrite(outpath, img)

        outpath = r'getBoxPoint.jpg'
        img = cv2.imread(path)
        img = resizeImg(img)
        binary_img = getCanny(img)
        max_contour, max_area = findMaxContour(binary_img)
        boxes = getBoxPoint(max_contour)
        for box in boxes:
            cv2.circle(img, tuple(box), 5, (0, 0, 255), 2)
        print(boxes)
        cv2.imwrite(outpath, img)

        outpath = r'result.jpg'
        image = cv2.imread(path)
        ratio = 900 / image.shape[0]
        img = resizeImg(image)
        binary_img = getCanny(img)
        max_contour, max_area = findMaxContour(binary_img)
        boxes = getBoxPoint(max_contour)
        boxes = adaPoint(boxes, ratio)
        boxes = orderPoints(boxes)
        # 透视变化
        warped = warpImage(image, boxes)
        cv2.imwrite(outpath, warped)

        img = cv2.imread('result.jpg')

        blurred = cv.pyrMeanShiftFiltering(img, 10, 10)  # 去除噪点
        # 中值模糊  对椒盐噪声有很好的去燥效果

        # 灰度图转化
        gray = cv.cvtColor(blurred, cv.COLOR_RGB2GRAY)
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

        # 图像反色
        img3 = cv.bitwise_not(img1)

        # 图像相乘
        img4 = cv.multiply(img3, img2)

        # 中值模糊  对椒盐噪声有很好的去燥效果
        img5 = cv.medianBlur(img4, 9)

        # 开闭运算去除不必要部分
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        mb = cv.morphologyEx(img5, cv.MORPH_OPEN, kernel, iterations=3)
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

        ret1, thresh = cv.threshold(img12, 35, 255, cv.THRESH_BINARY_INV)  # 118   125

        kerne1 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 形状 结构元素5*5
        # 腐蚀
        dst1 = cv.erode(thresh, kerne1)

        # 膨胀
        dst2 = cv.dilate(dst1, kerne1)

        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 返回指定的形状和元素 椭圆形
        open = cv.morphologyEx(dst2, cv.MORPH_OPEN, kernel, iterations=2)  # 形态学开操作

        # 膨胀# 对“开运算”的结果进行膨胀，得到大部分都是背景的区域
        sure_bg = cv.dilate(open, kernel, iterations=1)

        dist_tran = cv.distanceTransform(sure_bg, cv.DIST_L2, 3)  # 距离变换
        dist_output = cv.normalize(dist_tran, 0, 1.0, cv.NORM_MINMAX)  # 归一化在0~1之间

        # 前景获取：种子区域
        # ret1, surface = cv.threshold(dist_tran, 0.2*dist_tran.max(), 255, cv.THRESH_BINARY)
        ret1, surface = cv.threshold(dist_output, dist_output.max() * 0.2, 255, cv.THRESH_BINARY)  # 0.68 3
        # ret1, surface = cv.threshold(dist_tran, dist_tran.max() * 0.6, 255, 0)
        surface_fg = np.uint8(surface)

        # 未知区域：#除种子以外的区域
        unknown = cv.subtract(sure_bg, surface_fg)
        # 标记
        ret1, markers = cv.connectedComponents(
            surface_fg)  # 连通区域# ret: 计算最大连通域  连通域：是由具有相同像素值的相邻像素组成像素集合# makers：将图像的背景标记为0

        markers = markers + 1  # OpenCV 分水岭算法对物体做的标注必须都 大于1 ，背景为标号 为0  因此对所有markers 加1  变成了  1  -  N
        # 去掉属于背景区域的部分（即让其变为0，成为背景）
        # 此语句的Python语法 类似于if ，“unknow==255” 返回的是图像矩阵的真值表。
        markers[unknown == 255] = 0

        # Step8.分水岭算法
        markers = cv.watershed(img13, markers)  # 分水岭算法后，所有轮廓的像素点被标注为  -1

        img13[markers == -1] = [153, 51, 225]  # 标注为-1 的像素点标
        # cv.imshow('markeers',np.abs(markers))

        plt.imsave("biaoji.jpg", markers)
        img14 = cv.imread('biaoji.jpg')

        img15 = img14.copy()
        # img3 = np.zeros((img1.shape), dtype=np.uint8)
        # cv2.imwrite("C:/Users/Administrator/Desktop/2/3.jpg", img3)
        img16 = cv.addWeighted(img15, 0.4, img13, 0.7, 1)

        # path10 = r'C:/flask/tpchulijieguo1'
        # cv.imwrite(os.path.join(path10, '111.jpg'), img16)

        # 轮廓检测函数
        contours, hierarchy = cv.findContours(surface_fg, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        # 绘制轮廓
        cv.drawContours(surface_fg, contours, -1, (120, 0, 0), 2)

        count = 0  # 图像个数
        # 遍历找到的所有图像
        global ares
        for cont in contours:
            # 计算包围性状的面积
            ares = cv.contourArea(cont)
            mj = ares * 6.4516 * 4 / 10 / 5184
            # 过滤面积
            if ares < 50:
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

        print('可疑区域个数', count)
        cv.namedWindow("imagshow", 2)  # 创建一个窗口
        cv.imshow('imagshow', img16)  # 显示原始图片（添加了外接矩形）

        img_path3 = r'C:/flask/upload/000'

        RGA(img_path3)

        img1p3 = RGA(img_path3)

        img_path2 = r'C:/flask/upload/cs4'

        RGA2(img_path2)

        img2p = RGA2(img_path2)
        imgq1p = cv2.resize(img2p, (921, 1440))

        # img1=cv2.imread("C:/Users/Administrator/Desktop/xxy/9999.png")
        # img2=cv2.imread("C:/Users/Administrator/Desktop/xxy/01.png")
        img3p = cv2.add(img1p3, imgq1p)

        # cv2.imwrite("diejia.png",img3)

        # img3 = img3[136:289, 779:932]  # x0,y0为裁剪区域左上坐标；x1,y1为裁剪区域右下坐标
        cv2.imwrite('diejia1p.png', img3p)

        imgp = cv2.imread('diejia1p.png')  # img_path为图片所在路径
        img3p = imgp[289:932, 136:779]  # x0,y0为裁剪区域左上坐标；x1,y1为裁剪区域右下坐标
        cv2.imwrite("diejiap.png", img3p)  # save_path为保存路径

        global pathp
        pathp = r'diejiap.png'
        outpathp = r'getCannyp.jpg'
        imgp = cv2.imread(pathp)
        imgp = resizeImgp(imgp)
        print('shape =', imgp.shape)
        binary_imgp = getCannyp(imgp)
        cv2.imwrite(outpathp, binary_imgp)
        # output:    shape = (900, 420, 3)

        outpathp = r'findMaxContourp.jpg'
        imgp = cv2.imread(pathp)
        imgp = resizeImgp(imgp)
        binary_imgp = getCannyp(imgp)
        max_contourp, max_area = findMaxContourp(binary_imgp)
        cv2.drawContours(imgp, max_contourp, -1, (0, 0, 255), 3)
        cv2.imwrite(outpathp, imgp)

        outpathp = r'getBoxPointp.jpg'
        imgp = cv2.imread(pathp)
        imgp = resizeImgp(imgp)
        binary_imgp = getCannyp(imgp)
        max_contourp, max_area = findMaxContourp(binary_imgp)
        boxesp = getBoxPointp(max_contourp)
        for box in boxesp:
            cv2.circle(imgp, tuple(box), 5, (0, 0, 255), 2)
        print(boxesp)
        cv2.imwrite(outpathp, imgp)

        outpathp = r'resultp.jpg'
        image = cv2.imread(pathp)
        ratio = 900 / image.shape[0]
        imgp = resizeImgp(image)
        binary_imgp = getCannyp(imgp)
        max_contourp, max_area = findMaxContourp(binary_imgp)
        boxesp = getBoxPointp(max_contourp)
        boxesp = adaPointp(boxesp, ratio)
        boxesp = orderPointsp(boxesp)
        # 透视变化
        warpedp = warpImage(image, boxesp)
        cv2.imwrite(outpathp, warpedp)

        imgp = cv2.imread('resultp.jpg')

        blurredp = cv.pyrMeanShiftFiltering(imgp, 10, 10)  # 去除噪点
        # 中值模糊  对椒盐噪声有很好的去燥效果

        # 灰度图转化
        grayp = cv.cvtColor(blurredp, cv.COLOR_RGB2GRAY)
        img1p = grayp
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        mbp = cv.morphologyEx(img1p, cv.MORPH_OPEN, kernel, iterations=5)
        img6p = cv.morphologyEx(mbp, cv.MORPH_CLOSE, kernel, iterations=3)

        # 全局二值化
        ret, binaryp = cv.threshold(img6p, 198, 255, cv.THRESH_BINARY_INV)  # THRESH_OTSU自动阈值  方法不一样，阈值不一样（很有用，自己查！！！）
        # binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
        # ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

        img2p = binaryp

        # 图像反色
        img3p = cv.bitwise_not(img1p)

        # 图像相乘
        img4p = cv.multiply(img3p, img2p)

        # 中值模糊  对椒盐噪声有很好的去燥效果
        img5p = cv.medianBlur(img4p, 9)

        # 开闭运算去除不必要部分
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        mbp = cv.morphologyEx(img5p, cv.MORPH_OPEN, kernel, iterations=3)
        img6p = cv.morphologyEx(mbp, cv.MORPH_CLOSE, kernel, iterations=1)

        # 取反色
        img7p = cv.bitwise_not(img6p)

        # 图像相加
        img8p = cv.add(img1p, img7p)

        # 取反色
        img9p = cv.bitwise_not(img8p)

        # 相除
        img10p = cv.subtract(img6p, img9p)

        # rgb格式转化
        img11p = cv.cvtColor(img10p, cv.COLOR_RGB2RGBA)

        cv.imwrite("img13p.jpg", img11p)
        img13p = cv.imread('img13p.jpg')

        blurredp = cv.pyrMeanShiftFiltering(img13p, 5, 10)  # 去除噪点

        # 灰度
        img12p = cv.cvtColor(blurredp, cv.COLOR_BGR2GRAY)
        # 二值化

        ret1, threshp = cv.threshold(img12p, 35, 255, cv.THRESH_BINARY_INV)  # 118   125

        kerne1 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 形状 结构元素5*5
        # 腐蚀
        dst1p = cv.erode(threshp, kerne1)

        # 膨胀
        dst2p = cv.dilate(dst1p, kerne1)

        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 返回指定的形状和元素 椭圆形
        openp = cv.morphologyEx(dst2p, cv.MORPH_OPEN, kernel, iterations=2)  # 形态学开操作

        # 膨胀# 对“开运算”的结果进行膨胀，得到大部分都是背景的区域
        sure_bgp = cv.dilate(openp, kernel, iterations=1)

        dist_tranp = cv.distanceTransform(sure_bgp, cv.DIST_L2, 3)  # 距离变换
        dist_outputp = cv.normalize(dist_tranp, 0, 1.0, cv.NORM_MINMAX)  # 归一化在0~1之间

        # 前景获取：种子区域
        # ret1, surface = cv.threshold(dist_tran, 0.2*dist_tran.max(), 255, cv.THRESH_BINARY)
        ret1, surfacep = cv.threshold(dist_outputp, dist_outputp.max() * 0.2, 255, cv.THRESH_BINARY)  # 0.68 3
        # ret1, surface = cv.threshold(dist_tran, dist_tran.max() * 0.6, 255, 0)
        surface_fgp = np.uint8(surfacep)

        # 未知区域：#除种子以外的区域
        unknownp = cv.subtract(sure_bgp, surface_fgp)
        # 标记
        ret1, markersp = cv.connectedComponents(
            surface_fgp)  # 连通区域# ret: 计算最大连通域  连通域：是由具有相同像素值的相邻像素组成像素集合# makers：将图像的背景标记为0
        print(ret1)

        markersp = markersp + 1  # OpenCV 分水岭算法对物体做的标注必须都 大于1 ，背景为标号 为0  因此对所有markers 加1  变成了  1  -  N
        # 去掉属于背景区域的部分（即让其变为0，成为背景）
        # 此语句的Python语法 类似于if ，“unknow==255” 返回的是图像矩阵的真值表。
        markersp[unknownp == 255] = 0

        # Step8.分水岭算法
        markersp = cv.watershed(img13p, markersp)  # 分水岭算法后，所有轮廓的像素点被标注为  -1
        print(markersp)
        img13p[markersp == -1] = [153, 51, 225]  # 标注为-1 的像素点标
        # cv.imshow('markeers',np.abs(markers))

        plt.imsave("biaojip.jpg", markersp)
        img14p = cv.imread('biaojip.jpg')

        img15p = img14p.copy()
        # img3 = np.zeros((img1.shape), dtype=np.uint8)
        # cv2.imwrite("C:/Users/Administrator/Desktop/2/3.jpg", img3)
        img16p = cv.addWeighted(img15p, 0.4, img13p, 0.7, 1)

        path10 = r'C:/flask/tpchulijieguo1'
        cv.imwrite(os.path.join(path10, '111.jpg'), img16p)
        # 轮廓检测函数
        contoursp, hierarchy = cv.findContours(surface_fgp, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        # 绘制轮廓
        cv.drawContours(surface_fgp, contoursp, -1, (120, 0, 0), 2)

        count = 0  # 图像个数
        # 遍历找到的所有图像
        for cont in contoursp:
            # 计算包围性状的面积
            ares = cv.contourArea(cont)
            mj = ares * 6.4516 * 4 / 10 / 5184
            # 过滤面积
            if ares < 50:
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
            cv.rectangle(img16p, rect, (0, 0, 120), 0)

            # 防止编号到图片之外（上面）,因为绘制编号写在左上角，所以让最上面的图像的y小于10的变为10个像素
            y = 10 if rect[1] < 10 else rect[1]
            # 在图像左上角写上编号
            cv.putText(img16p, str(count), (rect[0], y), cv.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)
            # print('编号坐标：',rect[0],' ', y)

        print('可疑区域个数', count)
        cv.namedWindow("imagshowp", 2)  # 创建一个窗口
        cv.imshow('imagshowp', img16p)  # 显示原始图片（添加了外接矩形）
        check()
        del_file(img_path2)
        del_file(img_path1)


        # cv2.waitKey(0)
        # cv2.destroyAllWindows()




def RGA3(img_path, ):
    imgs_path = os.listdir(img_path)
    for r in imgs_path:
        global img
        img = os.path.join(img_path, r)
        img = cv.imread(img)
    return img


# 代码承接上文
# 求出面积最大的轮廓
def findMaxContour(image):
    # 寻找边缘
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 计算面积
    max_area = 0.0
    max_contour = []
    global currentArea
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > max_area:
            max_area = currentArea
            max_contour = contour
    return max_contour, max_area


def RGA1(img_path1, ):
    imgs_path = os.listdir(img_path1)
    for r in imgs_path:
        img = os.path.join(img_path1, r)
        img = cv.imread(img)
    return img





def resizeImg(image, height=900):
    h, w = image.shape[:2]
    pro = height / h
    size = (int(w * pro), int(height))
    img = cv2.resize(image, size)
    return img


# 边缘检测
def getCanny(image):
    # 高斯模糊
    binary = cv2.GaussianBlur(image, (3, 3), 1, 1)
    # 边缘检测
    binary = cv2.Canny(binary, 60, 240, apertureSize=3)
    # 膨胀操作，尽量使边缘闭合
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    return binary


# 代码承接上文
# 多边形拟合凸包的四个顶点
def getBoxPoint(contour):
    # 多边形拟合凸包
    hull = cv2.convexHull(contour)
    epsilon = 0.001 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(hull, epsilon, True)
    approx = approx.reshape((len(approx), 2))
    return approx


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
    M = cv2.getPerspectiveTransform(box, dst_rect)
    warped = cv2.warpPerspective(image, M, (w, h))
    return warped

def RGA(img_path, ):
    imgs_path = os.listdir(img_path)
    for r in imgs_path:
        global img
        img = os.path.join(img_path, r)
        img = cv.imread(img)
    return img

def RGA2(img_path1, ):
    imgs_path = os.listdir(img_path1)
    for r in imgs_path:
        global img
        img = os.path.join(img_path1, r)
        img = cv.imread(img)
    return img


def resizeImgp(image, height=900):
    h, w = image.shape[:2]
    pro = height / h
    size = (int(w * pro), int(height))
    img = cv2.resize(image, size)
    return img


# 边缘检测
def getCannyp(image):
    # 高斯模糊
    binary = cv2.GaussianBlur(image, (3, 3), 1, 1)
    # 边缘检测
    binary = cv2.Canny(binary, 60, 240, apertureSize=3)
    # 膨胀操作，尽量使边缘闭合
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    return binary


# 代码承接上文
# 求出面积最大的轮廓
def findMaxContourp(image):
    # 寻找边缘
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 计算面积
    max_area = 0.0
    max_contourp = []
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > max_area:
            max_area = currentArea
            max_contourp = contour
    return max_contourp, max_area


# 代码承接上文
# 多边形拟合凸包的四个顶点
def getBoxPointp(contour):
    # 多边形拟合凸包
    hull = cv2.convexHull(contour)
    epsilon = 0.001 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(hull, epsilon, True)
    approx = approx.reshape((len(approx), 2))
    return approx


# 代码承接上文
# 适配原四边形点集
def adaPointp(box, pro):
    box_pro = box
    if pro != 1.0:
        box_pro = box / pro
    box_pro = np.trunc(box_pro)
    return box_pro


# 四边形顶点排序，[top-left, top-right, bottom-right, bottom-left]
def orderPointsp(pts):
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
    M = cv2.getPerspectiveTransform(box, dst_rect)
    warped = cv2.warpPerspective(image, M, (w, h))
    return warped


# 创建一个txt文件，文件名为mytxtfile,并向文件写入msg
def text_create(name, msg):
    desktop_path = "C:/Users/Administrator/Desktop/"  # 新创建的txt文件的存放路径
    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w')
    file.write(msg)  # msg也就是下面的Hello world!
    # file.close()


def check():
    res = (currentArea - ares) / currentArea * 100
    print("res:{}".format(res))
    # print(res)
    if res > 0 and res < 20:
        text_create('mytxtfile3', '第一级：一级脑出血者一般没有明显症状或仅有轻度头痛和颈强直的情况，一般不需要治疗，但应避免情绪波动，戒烟戒酒。')
    if res > 20 and res < 40:
        text_create('mytxtfile3', '第二级：二级脑出血者可能会出现头痛或一侧肢体明显瘫痪的现象，容易导致运动能力下降及感觉异常。可使用阿司匹林片、丁苯酞软胶囊、对乙酰氨基酚片等药物缓解症状。')
    if res > 40 and res < 60:
        text_create('mytxtfile3', '第三级：三级脑出血者可能会出现轻度意识障碍，烦躁不安等症状。可在医生建议下使用药物再配合高压氧、理疗、针灸的方式治疗，促使脑功能恢复。')
    if res > 60 and res < 80:
        text_create('mytxtfile3',
                    '第四级：四级脑出血者可能会出现浅昏迷、偏侧肢体瘫痪、大脑强直和植物神经功能障碍的症状。一般需要通过去骨瓣减压术、小骨窗开颅血肿清除术、钻孔穿刺血肿碎吸术、内镜血肿清除术等手术方式治疗。同时还要注意术后护理，避免辛辣、刺激性食物')
    if res > 80 and res < 100:
        text_create('mytxtfile3', '第五级：五级脑出血者一般会出现深度昏迷的症状，应及时去医院就诊以免延误时间危及生命，配合医生积极治疗。同时还要注意饮食，多吃富含膳食纤维的食物，如红薯、西蓝花、蘑菇等')
    # 属于百分之？
    # return print(方案1)


# 删除文件夹下的文件&&保留但清空子文件夹
def del_file(filepath):
    print("hello")
    listdir = os.listdir(filepath)  # 获取文件和子文件夹
    print(listdir)
    for dirname in listdir:
        dirname = filepath + "//" + dirname
        if os.path.isfile(dirname):  # 是文件
            print(dirname)
            os.remove(dirname)  # 删除文件
        elif os.path.isdir(dirname):  # 是子文件夹
            print(dirname)
            dellist = os.listdir(dirname)
            for f in dellist:  # 遍历该子文件夹
                file_path = os.path.join(dirname, f)
                if os.path.isfile(file_path):  # 删除子文件夹下文件
                    os.remove(file_path)
                elif os.path.isdir(file_path):  # 强制删除子文件夹下的子文件夹
                    shutil.rmtree(file_path)


# check()
plt.show()
cv.waitKey(0)
cv.destroyAllWindows()


def on_deleted(self, event):
    if event.is_directory:
        print("directory deleted:{0}".format(event.src_path))
    else:
        print("file deleted:{0}".format(event.src_path))


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

