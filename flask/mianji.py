import time
import cv2 as cv
import numpy as np
import os
import shutil
import matplotlib.pyplot as plt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import matplotlib.pyplot as plt
from flask import Flask
import json
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


"""
mj = ares * 6.4516 * 4 / 10 / 5184  
"""
path = r'C:/flask/upload/cs2'



class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        img_path = r'C:/flask/upload/cs1'

        RGA(img_path)

        img = RGA(img_path)
        """
        #选择文件操作
        root = tk.Tk()
        root.withdraw()
        # FolderPath=filedialog.askdirectory() #选择文件夹用的
        FilePath = filedialog.askopenfilename()  # 选择文件用的
        # print('FolderPath:',FolderPath)#验证文件夹
        print('FilePath:', FilePath)  # 验证文件
        img=cv.imread(FilePath)
        """
        cv.imshow("0", img)
        print(img.shape)
        # 灰度图转化
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        cv.imshow("img1", gray)
        img1 = gray
        # 全局二值化
        ret, binary = cv.threshold(img1, 0, 255,
                                   cv.THRESH_BINARY | cv.THRESH_TRIANGLE)  # THRESH_OTSU自动阈值  方法不一样，阈值不一样（很有用，自己查！！！）
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
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
        mb = cv.morphologyEx(img5, cv.MORPH_OPEN, kernel, iterations=2)
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

        blurred = cv.pyrMeanShiftFiltering(img13, 10, 15)  # 去除噪点

        # 灰度
        img12 = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
        # 二值化

        ret1, thresh = cv.threshold(img12, 140, 255, cv.THRESH_BINARY)  # 118   125
        cv.imshow("erzhihua", thresh)

        kerne1 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 形状 结构元素5*5
        # 腐蚀
        dst1 = cv.erode(thresh, kerne1)
        cv.imshow("erode_demo", dst1)

        # 膨胀
        dst2 = cv.dilate(dst1, kerne1)

        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (4, 4))  # 返回指定的形状和元素 椭圆形
        open1 = cv.morphologyEx(dst2, cv.MORPH_OPEN, kernel, iterations=3)  # 形态学开操作
        cv.imshow("open1", open1)

        # 膨胀# 对“开运算”的结果进行膨胀，得到大部分都是背景的区域
        sure_bg = cv.dilate(open1, kernel, iterations=3)
        cv.imshow("beijing", sure_bg)

        dist_tran = cv.distanceTransform(sure_bg, cv.DIST_L2, 3)  # 距离变换
        dist_output = cv.normalize(dist_tran, 0, 1.0, cv.NORM_MINMAX)  # 归一化在0~1之间
        cv.imshow("dist_output", dist_output * 70)
        cv.imshow("dist_tran", dist_tran * 70)

        # 前景获取：种子区域
        # ret1, surface = cv.threshold(dist_tran, 0.2*dist_tran.max(), 255, cv.THRESH_BINARY)
        ret1, surface = cv.threshold(dist_output, dist_output.max() * 0.1, 255, cv.THRESH_BINARY)  # 0.68 3
        # ret1, surface = cv.threshold(dist_tran, dist_tran.max() * 0.6, 255, 0)
        surface_fg = np.uint8(surface)
        cv.imshow("surface", surface_fg)

        contours, hierarchy = cv.findContours(
            surface_fg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        global cnt
        cnt = contours[1]
        cv.drawContours(img, [cnt], 0, (0, 0, 255), 2)
        global area
        area = cv.contourArea(cnt)
        perimeter = cv.arcLength(cnt, True)  # True表示图像是否封闭
        print(area)  # 白色区域面积

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

        def RGA1(img_path1, ):
            imgs_path = os.listdir(img_path1)
            for r in imgs_path:
                img01 = os.path.join(img_path1, r)
                img01 = cv.imread(img01)
            return img01

        img_path1 = r'C:/flask/upload/cs2'

        RGA1(img_path1)

        img01 = RGA1(img_path1)
        """
        #选择文件操作
        root = tk.Tk()
        root.withdraw()
        # FolderPath=filedialog.askdirectory() #选择文件夹用的
        FilePath = filedialog.askopenfilename()  # 选择文件用的
        # print('FolderPath:',FolderPath)#验证文件夹
        print('FilePath:', FilePath)  # 验证文件
        img=cv.imread(FilePath)
        """
        cv.imshow("01", img01)
        print(img01.shape)
        # 灰度图转化
        gray1 = cv.cvtColor(img01, cv.COLOR_RGB2GRAY)
        cv.imshow("img01", gray1)
        img_1 = gray1
        # 全局二值化
        ret, binary01 = cv.threshold(img_1, 0, 255,
                                     cv.THRESH_BINARY | cv.THRESH_TRIANGLE)  # THRESH_OTSU自动阈值  方法不一样，阈值不一样（很有用，自己查！！！）
        # binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
        # ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
        print("threshold value %s" % ret)
        img02 = binary01
        cv.imshow("img02", img02)

        # 图像反色
        img03 = cv.bitwise_not(img_1)
        cv.imshow("img03", img03)

        # 图像相乘
        img04 = cv.multiply(img03, img02)
        cv.imshow("img04", img04)

        # 中值模糊  对椒盐噪声有很好的去燥效果
        img05 = cv.medianBlur(img04, 9)
        cv.imshow("img05", img05)

        # 开闭运算去除不必要部分
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
        mb01 = cv.morphologyEx(img05, cv.MORPH_OPEN, kernel, iterations=2)
        img06 = cv.morphologyEx(mb01, cv.MORPH_CLOSE, kernel, iterations=1)
        cv.imshow("img06", img06)

        # 取反色
        img07 = cv.bitwise_not(img06)
        cv.imshow("img07", img07)

        # 图像相加
        img08 = cv.add(img_1, img07)
        cv.imshow("img08", img08)

        # 取反色
        img09 = cv.bitwise_not(img08)
        cv.imshow("img09", img09)

        # 相除
        img010 = cv.subtract(img06, img09)
        cv.imshow("img010", img010)

        # rgb格式转化
        img011 = cv.cvtColor(img010, cv.COLOR_RGB2RGBA)
        cv.imshow("img011", img011)
        cv.imwrite("img013.jpg", img011)
        img013 = cv.imread('img013.jpg')
        print(img013.shape)

        blurred0 = cv.pyrMeanShiftFiltering(img013, 10, 15)  # 去除噪点

        # 灰度
        img012 = cv.cvtColor(blurred0, cv.COLOR_BGR2GRAY)
        # 二值化

        ret1, thresh0 = cv.threshold(img012, 140, 255, cv.THRESH_BINARY)  # 118   125
        cv.imshow("erzhihua0", thresh0)

        kerne1 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 形状 结构元素5*5
        # 腐蚀
        dst01 = cv.erode(thresh0, kerne1)
        cv.imshow("erode_demo0", dst01)

        # 膨胀
        dst02 = cv.dilate(dst01, kerne1)

        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (4, 4))  # 返回指定的形状和元素 椭圆形
        open0 = cv.morphologyEx(dst02, cv.MORPH_OPEN, kernel, iterations=3)  # 形态学开操作
        cv.imshow("open0", open0)

        # 膨胀# 对“开运算”的结果进行膨胀，得到大部分都是背景的区域
        sure_bg0 = cv.dilate(open0, kernel, iterations=3)
        cv.imshow("beijing0", sure_bg0)

        dist_tran0 = cv.distanceTransform(sure_bg0, cv.DIST_L2, 3)  # 距离变换
        dist_output0 = cv.normalize(dist_tran0, 0, 1.0, cv.NORM_MINMAX)  # 归一化在0~1之间
        cv.imshow("dist_output0", dist_output0 * 70)
        cv.imshow("dist_tran0", dist_tran0 * 70)

        # 前景获取：种子区域
        # ret1, surface = cv.threshold(dist_tran, 0.2*dist_tran.max(), 255, cv.THRESH_BINARY)
        ret1, surface0 = cv.threshold(dist_output0, dist_output0.max() * 0.1, 255, cv.THRESH_BINARY)  # 0.68 3
        # ret1, surface = cv.threshold(dist_tran, dist_tran.max() * 0.6, 255, 0)
        surface_fg0 = np.uint8(surface0)
        cv.imshow("surface0", surface_fg0)

        # 未知区域：#除种子以外的区域
        unknown = cv.subtract(sure_bg, surface_fg0)
        # 标记
        ret1, markers0 = cv.connectedComponents(
            surface_fg0)  # 连通区域# ret: 计算最大连通域  连通域：是由具有相同像素值的相邻像素组成像素集合# makers：将图像的背景标记为0

        markers0 = markers0 + 1  # OpenCV 分水岭算法对物体做的标注必须都 大于1 ，背景为标号 为0  因此对所有markers 加1  变成了  1  -  N
        # 去掉属于背景区域的部分（即让其变为0，成为背景）
        # 此语句的Python语法 类似于if ，“unknow==255” 返回的是图像矩阵的真值表。
        markers0[unknown == 255] = 0

        # Step8.分水岭算法
        markers0 = cv.watershed(img013, markers0)  # 分水岭算法后，所有轮廓的像素点被标注为  -1

        img013[markers0 == -1] = [153, 51, 225]  # 标注为-1 的像素点标
        # cv.imshow('markeers',np.abs(markers))

        plt.imsave("biaoji0.jpg", markers0)
        img014 = cv.imread('biaoji0.jpg')

        img015 = img014.copy()
        # img3 = np.zeros((img1.shape), dtype=np.uint8)
        # cv2.imwrite("C:/Users/Administrator/Desktop/2/3.jpg", img3)
        img016 = cv.addWeighted(img015, 0.4, img013, 0.7, 1)

        # 轮廓检测函数
        contours0, hierarchy = cv.findContours(surface_fg0, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        # 绘制轮廓
        cv.drawContours(surface_fg0, contours0, -1, (120, 0, 0), 2)

        count = 0  # 图像个数
        # 遍历找到的所有图像
        for cont in contours0:
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
            cv.rectangle(img016, rect, (0, 0, 120), 0)

            # 防止编号到图片之外（上面）,因为绘制编号写在左上角，所以让最上面的图像的y小于10的变为10个像素
            y = 10 if rect[1] < 10 else rect[1]
            # 在图像左上角写上编号
            cv.putText(img016, str(count), (rect[0], y), cv.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)
            # print('编号坐标：',rect[0],' ', y)

        print('可疑区域个数', count)
        cv.namedWindow("imagshow", 0)  # 创建一个窗口
        cv.imshow('imagshow0', img016)  # 显示原始图片（添加了外接矩形）

        contours1, hierarchy1 = cv.findContours(
            surface_fg0, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        global cnt1
        cnt1 = contours1[1]
        cv.drawContours(img01, [cnt1], 0, (0, 0, 255), 2)
        global area1
        area1 = cv.contourArea(cnt1)
        perimeter = cv.arcLength(cnt1, True)  # True表示图像是否封闭
        print(area1)  # 白色区域面积
        check()
        del_file(img_path)
        del_file(img_path1)



def RGA(img_path,):
    imgs_path = os.listdir(img_path)
    for r in imgs_path:
        global img
        img=os.path.join(img_path,r)
        img = cv.imread(img)
    return img
#
# img_path=r'C:/cs/cs1'
#
# RGA(img_path)
#
# img=RGA(img_path)
# """
# #选择文件操作
# root = tk.Tk()
# root.withdraw()
# # FolderPath=filedialog.askdirectory() #选择文件夹用的
# FilePath = filedialog.askopenfilename()  # 选择文件用的
# # print('FolderPath:',FolderPath)#验证文件夹
# print('FilePath:', FilePath)  # 验证文件
# img=cv.imread(FilePath)
# """
# cv.imshow("0",img)
# print(img.shape)
# #灰度图转化
# gray = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
# cv.imshow("img1",gray)
# img1=gray
# #全局二值化
# ret, binary = cv.threshold(img1, 0, 255, cv.THRESH_BINARY|cv.THRESH_TRIANGLE)#THRESH_OTSU自动阈值  方法不一样，阈值不一样（很有用，自己查！！！）
# #binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
# #ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
# print("threshold value %s"%ret)
# img2=binary
# cv.imshow("img2", img2)
#
# # 图像反色
# img3 = cv.bitwise_not(img1)
# cv.imshow("img3", img3)
#
# #图像相乘
# img4 = cv.multiply(img3, img2)
# cv.imshow("img4", img4)
#
# # 中值模糊  对椒盐噪声有很好的去燥效果
# img5 = cv.medianBlur(img4, 9)
# cv.imshow("img5", img5)
#
# #开闭运算去除不必要部分
# kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
# mb = cv.morphologyEx(img5, cv.MORPH_OPEN, kernel, iterations=2)
# img6= cv.morphologyEx(mb, cv.MORPH_CLOSE, kernel, iterations=1)
# cv.imshow("img6", img6)
#
# #取反色
# img7 = cv.bitwise_not(img6)
# cv.imshow("img7", img7)
#
# #图像相加
# img8 = cv.add(img1,img7)
# cv.imshow("img8", img8)
#
# #取反色
# img9 = cv.bitwise_not(img8)
# cv.imshow("img9", img9)
#
# #相除
# img10 = cv.subtract(img6,img9)
# cv.imshow("img10", img10)
#
# #rgb格式转化
# img11= cv.cvtColor(img10, cv.COLOR_RGB2RGBA)
# cv.imshow("img11", img11)
# cv.imwrite("img13.jpg",img11)
# img13=cv.imread('img13.jpg')
# print(img13.shape)
#
#
# blurred = cv.pyrMeanShiftFiltering(img13,10,15)  #去除噪点
#
# #灰度
# img12 = cv.cvtColor(blurred,cv.COLOR_BGR2GRAY)
# #二值化
#
# ret1, thresh = cv.threshold(img12, 140, 255, cv.THRESH_BINARY)#118   125
# cv.imshow("erzhihua", thresh)
#
# kerne1 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))# 形状 结构元素5*5
# #腐蚀
# dst1 = cv.erode(thresh, kerne1)
# cv.imshow("erode_demo", dst1)
#
# # 膨胀
# dst2 = cv.dilate(dst1, kerne1)
#
# kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (4, 4))#返回指定的形状和元素 椭圆形
# open1= cv.morphologyEx(dst2 , cv.MORPH_OPEN, kernel, iterations=3)  # 形态学开操作
# cv.imshow("open1", open1)
#
# # 膨胀# 对“开运算”的结果进行膨胀，得到大部分都是背景的区域
# sure_bg = cv.dilate(open1, kernel, iterations=3)
# cv.imshow("beijing", sure_bg)
#
# dist_tran = cv.distanceTransform(sure_bg, cv.DIST_L2, 3)  # 距离变换
# dist_output = cv.normalize(dist_tran, 0, 1.0, cv.NORM_MINMAX)  # 归一化在0~1之间
# cv.imshow("dist_output", dist_output * 70)
# cv.imshow("dist_tran", dist_tran * 70)
#
# #前景获取：种子区域
# #ret1, surface = cv.threshold(dist_tran, 0.2*dist_tran.max(), 255, cv.THRESH_BINARY)
# ret1, surface = cv.threshold(dist_output, dist_output.max() * 0.1, 255, cv.THRESH_BINARY)#0.68 3
# #ret1, surface = cv.threshold(dist_tran, dist_tran.max() * 0.6, 255, 0)
# surface_fg = np.uint8(surface)
# cv.imshow("surface",surface_fg)
#
# contours, hierarchy = cv.findContours(
#     surface_fg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# global cnt
# cnt = contours[1]
# cv.drawContours(img, [cnt], 0, (0, 0, 255), 2)
# global area
# area = cv.contourArea(cnt)
# perimeter = cv.arcLength(cnt, True)#True表示图像是否封闭
# print(area)#白色区域面积


def RGA1(img_path1,):
    imgs_path = os.listdir(img_path1)
    for r in imgs_path:
        global img01
        img01=os.path.join(img_path1,r)
        img01 = cv.imread(img01)
    return img01
#
# img_path1=r'C:/cs/cs2'
#
# RGA1(img_path1)
#
# img01=RGA1(img_path1)
# """
# #选择文件操作
# root = tk.Tk()
# root.withdraw()
# # FolderPath=filedialog.askdirectory() #选择文件夹用的
# FilePath = filedialog.askopenfilename()  # 选择文件用的
# # print('FolderPath:',FolderPath)#验证文件夹
# print('FilePath:', FilePath)  # 验证文件
# img=cv.imread(FilePath)
# """
# cv.imshow("01",img01)
# print(img01.shape)
# #灰度图转化
# gray1 = cv.cvtColor(img01,cv.COLOR_RGB2GRAY)
# cv.imshow("img01",gray1)
# img_1=gray1
# #全局二值化
# ret, binary01 = cv.threshold(img_1, 0, 255, cv.THRESH_BINARY|cv.THRESH_TRIANGLE)#THRESH_OTSU自动阈值  方法不一样，阈值不一样（很有用，自己查！！！）
# #binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
# #ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
# print("threshold value %s"%ret)
# img02=binary01
# cv.imshow("img02", img02)
#
# # 图像反色
# img03 = cv.bitwise_not(img_1)
# cv.imshow("img03", img03)
#
# #图像相乘
# img04 = cv.multiply(img03, img02)
# cv.imshow("img04", img04)
#
# # 中值模糊  对椒盐噪声有很好的去燥效果
# img05 = cv.medianBlur(img04, 9)
# cv.imshow("img05", img05)
#
# #开闭运算去除不必要部分
# kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
# mb01 = cv.morphologyEx(img05, cv.MORPH_OPEN, kernel, iterations=2)
# img06= cv.morphologyEx(mb01, cv.MORPH_CLOSE, kernel, iterations=1)
# cv.imshow("img06", img06)
#
# #取反色
# img07 = cv.bitwise_not(img06)
# cv.imshow("img07", img07)
#
# #图像相加
# img08 = cv.add(img_1,img07)
# cv.imshow("img08", img08)
#
# #取反色
# img09 = cv.bitwise_not(img08)
# cv.imshow("img09", img09)
#
# #相除
# img010 = cv.subtract(img06,img09)
# cv.imshow("img010", img010)
#
# #rgb格式转化
# img011= cv.cvtColor(img010, cv.COLOR_RGB2RGBA)
# cv.imshow("img011", img011)
# cv.imwrite("img013.jpg",img011)
# img013=cv.imread('img013.jpg')
# print(img013.shape)
#
#
# blurred0 = cv.pyrMeanShiftFiltering(img013,10,15)  #去除噪点
#
# #灰度
# img012 = cv.cvtColor(blurred0,cv.COLOR_BGR2GRAY)
# #二值化
#
# ret1, thresh0 = cv.threshold(img012, 140, 255, cv.THRESH_BINARY)#118   125
# cv.imshow("erzhihua0", thresh0)
#
# kerne1 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))# 形状 结构元素5*5
# #腐蚀
# dst01 = cv.erode(thresh0, kerne1)
# cv.imshow("erode_demo0", dst01)
#
# # 膨胀
# dst02 = cv.dilate(dst01, kerne1)
#
# kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (4, 4))#返回指定的形状和元素 椭圆形
# open0= cv.morphologyEx(dst02 , cv.MORPH_OPEN, kernel, iterations=3)  # 形态学开操作
# cv.imshow("open0", open0)
#
# # 膨胀# 对“开运算”的结果进行膨胀，得到大部分都是背景的区域
# sure_bg0 = cv.dilate(open0, kernel, iterations=3)
# cv.imshow("beijing0", sure_bg0)
#
# dist_tran0 = cv.distanceTransform(sure_bg0, cv.DIST_L2, 3)  # 距离变换
# dist_output0 = cv.normalize(dist_tran0, 0, 1.0, cv.NORM_MINMAX)  # 归一化在0~1之间
# cv.imshow("dist_output0", dist_output0 * 70)
# cv.imshow("dist_tran0", dist_tran0 * 70)
#
# #前景获取：种子区域
# #ret1, surface = cv.threshold(dist_tran, 0.2*dist_tran.max(), 255, cv.THRESH_BINARY)
# ret1, surface0 = cv.threshold(dist_output0, dist_output0.max() * 0.1, 255, cv.THRESH_BINARY)#0.68 3
# #ret1, surface = cv.threshold(dist_tran, dist_tran.max() * 0.6, 255, 0)
# surface_fg0 = np.uint8(surface0)
# cv.imshow("surface0",surface_fg0)
#
# contours1, hierarchy1 = cv.findContours(
#     surface_fg0, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# global cnt1
# cnt1 = contours1[1]
# cv.drawContours(img01, [cnt1], 0, (0, 0, 255), 2)
# global area1
# area1 = cv.contourArea(cnt1)
# perimeter = cv.arcLength(cnt1, True)#True表示图像是否封闭
# print(area1)#白色区域面积


"""
01:

if （area-area1）/area *100% 
        属于百分之？
    return print(方案1)





"""


# 创建一个txt文件，文件名为mytxtfile,并向文件写入msg
def text_create(name, msg):
    desktop_path = "C:/Users/Administrator/Desktop/"  # 新创建的txt文件的存放路径
    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w')
    file.write(msg)  # msg也就是下面的Hello world!
    # file.close()

def check():
    res = (area-area1) / area * 100
    print("res:{}".format(res))
    # print(res)
    if res > 0 and res < 20:
        text_create('mytxtfile', '第一级：一级脑出血者一般没有明显症状或仅有轻度头痛和颈强直的情况，一般不需要治疗，但应避免情绪波动，戒烟戒酒。')
    if res > 20 and res < 40:
        text_create('mytxtfile', '第二级：二级脑出血者可能会出现头痛或一侧肢体明显瘫痪的现象，容易导致运动能力下降及感觉异常。可使用阿司匹林片、丁苯酞软胶囊、对乙酰氨基酚片等药物缓解症状。')
    if res > 40 and res < 60:
        text_create('mytxtfile', '第三级：三级脑出血者可能会出现轻度意识障碍，烦躁不安等症状。可在医生建议下使用药物再配合高压氧、理疗、针灸的方式治疗，促使脑功能恢复。')
    if res > 60 and res < 80:
        text_create('mytxtfile', '第四级：四级脑出血者可能会出现浅昏迷、偏侧肢体瘫痪、大脑强直和植物神经功能障碍的症状。一般需要通过去骨瓣减压术、小骨窗开颅血肿清除术、钻孔穿刺血肿碎吸术、内镜血肿清除术等手术方式治疗。同时还要注意术后护理，避免辛辣、刺激性食物')
    if res > 80 and res < 100:
        text_create('mytxtfile', '第五级：五级脑出血者一般会出现深度昏迷的症状，应及时去医院就诊以免延误时间危及生命，配合医生积极治疗。同时还要注意饮食，多吃富含膳食纤维的食物，如红薯、西蓝花、蘑菇等')
    #属于百分之？
    #return print(方案1)

 # 删除文件夹下的文件&&保留但清空子文件夹
def del_file(filepath):
    print("hello")
    listdir = os.listdir(filepath)  # 获取文件和子文件夹
    print(listdir)
    for dirname in listdir:
        dirname = filepath + "//" + dirname
        if os.path.isfile(dirname): # 是文件
            print(dirname)
            os.remove(dirname)      # 删除文件
        elif os.path.isdir(dirname):        # 是子文件夹
            print(dirname)
            dellist = os.listdir(dirname)
            for f in dellist:               # 遍历该子文件夹
                file_path = os.path.join(dirname, f)
                if os.path.isfile(file_path):       # 删除子文件夹下文件
                    os.remove(file_path)
                elif os.path.isdir(file_path):      # 强制删除子文件夹下的子文件夹
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