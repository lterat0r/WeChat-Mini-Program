# coding:utf-8
import json
import time as t
from werkzeug.utils import secure_filename
import os
import matplotlib.pyplot as plt
import base64
from flask import Flask,Response
#from flask_restful import Api, Resource, reqparse
import time
#import requests
#import jsonify
from flask import render_template,request,redirect,url_for
from flask import Flask, make_response
from flask_caching import Cache
import cv2
#import uri
#import roles
'''

配置上传目录，前端图片会上传到此目录下,
app.config['UPLOAD_FOLDER'] = 'upload/'

templates目录存放html文件

static目录存放html文件渲染的图片资源等，此目录下资源可通过url直接访问得到（如：http://192.168.3.7:5000/static/3.jpg)

logs输出日志



'''


UPLOADED_PHOTOS_DEST = './images/'  # 相对路径下的文件夹images
# UPLOADED_PHOTO_ALLOW = IMAGES       # 限制只能够上传图片

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/tupian/'
app.config['UPLOAD_FOLDER1'] = 'upload/cs1/'
app.config['UPLOAD_FOLDER2'] = 'upload/cs2/'
app.config['UPLOAD_FOLDER3'] = 'upload/tupian1/'
app.config['UPLOAD_FOLDER4'] = 'upload/cs3/'
app.config['UPLOAD_FOLDER5'] = 'upload/cs4/'
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 600,
    "CACHE_REDIS_HOST": "127.0.0.1",
    "CACHE_REDIS_PORT": '6379',
    "CACHE_REDIS_DB": 0,
}

app.config.from_mapping(config)
cache = Cache(app)

@app.route("/uploader5", methods=["GET", "POST"])
def upload5():

    if request.method == 'POST':
        start_time = t.time()
        f = request.files['file']
        if f is None:
            return "图片上传失败(failed)"
        global file_path
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER5'], filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER5'], filename))
        end_time = t.time()
        used_time = end_time - start_time
        print(file_path + '图片用时%.3f s上传成功(file upload successfully)' % used_time)
        time.sleep(1)

        data = {
            "code": 5201314,
            "msg": "success",
            "data":filename
        }
        return json.dumps(data)
    else:
        data = {
            "code": 405,
            "msg": "Method Not Allowed"
        }
        return json.dumps(data)



@app.route("/uploader4", methods=["GET", "POST"])
def upload4():

    if request.method == 'POST':
        start_time = t.time()
        f = request.files['file']
        if f is None:
            return "图片上传失败(failed)"
        global file_path
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER4'], filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER4'], filename))
        end_time = t.time()
        used_time = end_time - start_time
        print(file_path + '图片用时%.3f s上传成功(file upload successfully)' % used_time)
        time.sleep(1)

        data = {
            "code": 5201314,
            "msg": "success",
            "data":filename
        }
        return json.dumps(data)
    else:
        data = {
            "code": 405,
            "msg": "Method Not Allowed"
        }
        return json.dumps(data)


@app.route("/uploader3", methods=["GET", "POST"])
def upload3():

    if request.method == 'POST':
        start_time = t.time()
        f = request.files['file']
        if f is None:
            return "图片上传失败(failed)"
        global file_path
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER3'], filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER3'], filename))
        end_time = t.time()
        used_time = end_time - start_time
        print(file_path + '图片用时%.3f s上传成功(file upload successfully)' % used_time)
        time.sleep(1)

        data = {
            "code": 5201314,
            "msg": "success",
            "data":filename
        }
        return json.dumps(data)
    else:
        data = {
            "code": 405,
            "msg": "Method Not Allowed"
        }
        return json.dumps(data)

@app.route("/uploader2", methods=["GET", "POST"])
def upload2():

    if request.method == 'POST':
        start_time = t.time()
        f = request.files['file']
        if f is None:
            return "图片上传失败(failed)"
        global file_path
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER2'], filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
        end_time = t.time()
        used_time = end_time - start_time
        print(file_path + '图片用时%.3f s上传成功(file upload successfully)' % used_time)
        time.sleep(1)

        data = {
            "code": 5201314,
            "msg": "success",
            "data":filename
        }
        return json.dumps(data)
    else:
        data = {
            "code": 405,
            "msg": "Method Not Allowed"
        }
        return json.dumps(data)

@app.route("/uploader1", methods=["GET", "POST"])
def upload1():

    if request.method == 'POST':
        start_time = t.time()
        f = request.files['file']
        if f is None:
            return "图片上传失败(failed)"
        global file_path
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER1'], filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
        end_time = t.time()
        used_time = end_time - start_time
        print(file_path + '图片用时%.3f s上传成功(file upload successfully)' % used_time)
        time.sleep(1)

        data = {
            "code": 5201314,
            "msg": "success",
            "data":filename
        }
        return json.dumps(data)
    else:
        data = {
            "code": 405,
            "msg": "Method Not Allowed"
        }
        return json.dumps(data)



@app.route("/uploader", methods=["GET", "POST"])
def upload():

    if request.method == 'POST':
        start_time = t.time()
        f = request.files['file']
        if f is None:
            return "图片上传失败(failed)"
        global file_path
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        end_time = t.time()
        used_time = end_time - start_time
        print(file_path + '图片用时%.3f s上传成功(file upload successfully)' % used_time)
        time.sleep(1)

        data = {
            "code": 5201314,
            "msg": "success",
            "data":filename
        }
        return json.dumps(data)
    else:
        data = {
            "code": 405,
            "msg": "Method Not Allowed"
        }
        return json.dumps(data)

'''#base64
        path = r"C:\flask\tpchulijieguo\111.jpg"
        f = open(path, 'rb')
        base64_str = base64.b64encode(f.read())
        print("okok")
        return ( base64_str)'''


@app.route("/uploader/<imageId>.jpg")

def get_frame(imageId):
    # 图片上传保存的路径

    with open(r"C:\flask\tpchulijieguo\111.jpg".format(imageId), 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")

        return resp

@app.route("/uploader1/<imageId>.jpg")

def get_frame1(imageId):
    # 图片上传保存的路径

    with open(r"C:\flask\tpchulijieguo1\111.jpg".format(imageId), 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")

        return resp






@app.route("/getdata/<name>",methods=["GET", "POST"])
def get_data(name):
    print(name)
    arrname = name.split('.')
    ret = {
        "code": -1,
        "msg": "error",
        "data": []
    }
    data = cache.get(arrname[0])
    if data:
        ret = {
            "code": 0,
            "msg": "success",
            "data": json.loads(data)
        }
    return json.dumps(ret)


#二进制
        #with open("D:/flask/upload/tpchucun/imgshow.jpg", 'rb') as f:
         #     image = f.read()
          #      return Response(image, mimetype='image/jpeg')




        ################  do something  图像处理啥的   ################
'''@app.route("/uploader/transmission", methods=["GET", "POST"])
def uploader():
    app.config['UPLOAD_FOLDER'] = 'upload/tpceshi/'
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
            "code": 5201314,
            "msg": "success"
        }
        return json.dumps(data)
    else:
        data = {
            "code": 405,
            "msg": "Method Not Allowed"
        }
        return json.dumps(data)'''


@app.route("/uploader/transmission", methods=["GET", "POST"])
def uploader():

    with open(r'C:/flask/tupianchuli/2022-02-27-00-14-49_111.jpg', 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")
        return resp

#  请求地址为ip+/get_phone,当前端请求该地址时候执行down函数
@app.route("/get_phone", methods=["GET", "POST"])
def down():
    # 判断如果为POST方法则执行一下语句
    if request.method == 'POST':
        # 打开你的文本文件并且读
        file = open('C:/Users/Administrator/Desktop/mytxtfile.txt', 'r')  # 打开文件
        file_data = file.readlines()  # 读取所有行
        # 如果有多行数据将一行一行读取
        for row in file_data:
            tmp_lists = row.split(' ')  # 按‘，’切分每行的数据
            print(tmp_lists)
    # 返回为json数据传到前端
    return json.dumps(tmp_lists[0], ensure_ascii=False)

@app.route("/get_phone1", methods=["GET", "POST"])
def down1():
    # 判断如果为POST方法则执行一下语句
    if request.method == 'POST':
        # 打开你的文本文件并且读
        file = open('C:/Users/Administrator/Desktop/mytxtfile1.txt', 'r')  # 打开文件
        file_data = file.readlines()  # 读取所有行
        # 如果有多行数据将一行一行读取
        for row in file_data:
            tmp_lists = row.split(' ')  # 按‘，’切分每行的数据
            print(tmp_lists)
    # 返回为json数据传到前端
    return json.dumps(tmp_lists[0], ensure_ascii=False)

@app.route("/muzi/666", methods=["GET", "POST"])
def image1():

    with open(r'C:\Users\Administrator\Desktop\image111\CTtuduizhun.png', 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")
        return resp

@app.route("/muzi/666/1", methods=["GET", "POST"])
def image2():

    with open(r'C:\Users\Administrator\Desktop\image111\按钮.png', 'rb') as k:
        image1 = k.read()
        html = Response(image1, mimetype="image/jpg")
        return html

@app.route("/muzi/666/toushu", methods=["GET", "POST"])
def image3():
    with open(r'C:\wechartphoto\toushu.jpg', 'rb') as k:
        image2 = k.read()
        toushu = Response(image2, mimetype="image/jpg")
        return toushu
@app.route("/muzi/666/yaoping", methods=["GET", "POST"])
def image4():
    with open(r'C:\wechartphoto\yaoping.jpg', 'rb') as k:
        image3 = k.read()
        yaoping = Response(image3, mimetype="image/jpg")
        return yaoping
@app.route("/muzi/666/zhiliao", methods=["GET", "POST"])
def image5():
    with open(r'C:\wechartphoto\zhiliao.jpg', 'rb') as k:
        image5 = k.read()
        zhiliao = Response(image5, mimetype="image/jpg")
        return zhiliao
@app.route("/muzi/666/yingshi", methods=["GET", "POST"])
def image6():
    with open(r'C:\wechartphoto\yingshi.jpg', 'rb') as k:
        image6 = k.read()
        yingshi = Response(image6, mimetype="image/jpg")
        return yingshi
@app.route("/muzi/666/biaoti", methods=["GET", "POST"])
def image7():
    with open(r'C:\wechartphoto\biaoti.jpg', 'rb') as k:
        image7 = k.read()
        biaoti = Response(image7, mimetype="image/jpg")
        return biaoti
@app.route("/muzi/666/huoqutupian", methods=["GET", "POST"])
def image8():
    with open(r'C:\wechartphoto\huoqutupian.jpg', 'rb') as k:
        image8 = k.read()
        huoqutupian = Response(image8, mimetype="image/jpg")
        return huoqutupian
@app.route("/muzi/666/fenxijianyi", methods=["GET", "POST"])
def image9():
    with open(r'C:\wechartphoto\fenxijianyi.jpg', 'rb') as k:
        image9 = k.read()
        fenxijianyi = Response(image9, mimetype="image/jpg")
        return fenxijianyi
@app.route("/muzi/666/rengongzhineng", methods=["GET", "POST"])
def image10():
    with open(r'C:\wechartphoto\人工算法.jpg', 'rb') as k:
        image10 = k.read()
        rengongzhineng = Response(image10, mimetype="image/jpg")
        return rengongzhineng
@app.route("/muzi/666/beijing", methods=["GET", "POST"])
def image11():
    with open(r'C:\wechartphoto\beijing.jpg', 'rb') as k:
        image11 = k.read()
        beijing = Response(image11, mimetype="image/jpg")
        return beijing
@app.route("/muzi/666/yundongzhuyi1", methods=["GET", "POST"])
def image12():
    with open(r'C:\wechartphoto\yundongzhuyi1.jpg', 'rb') as k:
        image12 = k.read()
        yundongzhuyi1 = Response(image12, mimetype="image/jpg")
        return yundongzhuyi1
@app.route("/muzi/666/jinjishixiang", methods=["GET", "POST"])
def image13():
    with open(r'C:\wechartphoto\jinjishixiang.jpg', 'rb') as k:
        image13 = k.read()
        jinjishixiang = Response(image13, mimetype="image/jpg")
        return jinjishixiang
@app.route("/muzi/666/yongyaozhuyi1", methods=["GET", "POST"])
def image14():
    with open(r'C:\wechartphoto\yongyaozhuyi1.jpg', 'rb') as k:
        image14 = k.read()
        yongyaozhuyi1 = Response(image14, mimetype="image/jpg")
        return yongyaozhuyi1
@app.route("/muzi/666/tuoshuiyao", methods=["GET", "POST"])
def image15():
    with open(r'C:\wechartphoto\tuoshuiyao.jpg', 'rb') as k:
        image15 = k.read()
        tuoshuiyao = Response(image15, mimetype="image/jpg")
        return tuoshuiyao
@app.route("/muzi/666/kongzhixueya", methods=["GET", "POST"])
def image16():
    with open(r'C:\wechartphoto\kongzhixueya.jpg', 'rb') as k:
        image16 = k.read()
        kongzhixueya = Response(image16, mimetype="image/jpg")
        return kongzhixueya
@app.route("/muzi/666/naobaohuji", methods=["GET", "POST"])
def image17():
    with open(r'C:\wechartphoto\naobaohuji.jpg', 'rb') as k:
        image17 = k.read()
        naobaohuji = Response(image17, mimetype="image/jpg")
        return naobaohuji
@app.route("/muzi/666/zhixueyaowu", methods=["GET", "POST"])
def image18():
    with open(r'C:\wechartphoto\zhixueyaowu.jpg', 'rb') as k:
        image18 = k.read()
        zhixueyaowu = Response(image18, mimetype="image/jpg")
        return zhixueyaowu
@app.route("/muzi/666/huoxuehuayu", methods=["GET", "POST"])
def image19():
    with open(r'C:\wechartphoto\huoxuehuayu.jpg', 'rb') as k:
        image19 = k.read()
        huoxuehuayu = Response(image19, mimetype="image/jpg")
        return huoxuehuayu
@app.route("/muzi/666/yidaosu", methods=["GET", "POST"])
def image20():
    with open(r'C:\wechartphoto\yidaosu.jpg', 'rb') as k:
        image20 = k.read()
        yidaosu = Response(image20, mimetype="image/jpg")
        return yidaosu
@app.route("/muzi/666/tuoshuiyao1", methods=["GET", "POST"])
def image21():
    with open(r'C:\wechartphoto\tuoshuiyao1.jpg', 'rb') as k:
        image21 = k.read()
        tuoshuiyao1 = Response(image21, mimetype="image/jpg")
        return tuoshuiyao1
@app.route("/muzi/666/kongzhixueya1", methods=["GET", "POST"])
def image22():
    with open(r'C:\wechartphoto\kongzhixueya1.jpg', 'rb') as k:
        image22 = k.read()
        kongzhixueya1 = Response(image22, mimetype="image/jpg")
        return kongzhixueya1
@app.route("/muzi/666/naobaohuji1", methods=["GET", "POST"])
def image23():
    with open(r'C:\wechartphoto\naobaohuji1.jpg', 'rb') as k:
        image23 = k.read()
        naobaohuji1 = Response(image23, mimetype="image/jpg")
        return naobaohuji1
@app.route("/muzi/666/zhixueyaowu1", methods=["GET", "POST"])
def image24():
    with open(r'C:\wechartphoto\zhixueyaowu1.jpg', 'rb') as k:
        image24 = k.read()
        zhixueyaowu1 = Response(image24, mimetype="image/jpg")
        return zhixueyaowu1
@app.route("/muzi/666/huoxuehuayu1", methods=["GET", "POST"])
def image25():
    with open(r'C:\wechartphoto\huoxuehuayu1.jpg', 'rb') as k:
        image25 = k.read()
        huoxuehuayu1 = Response(image25, mimetype="image/jpg")
        return huoxuehuayu1
@app.route("/muzi/666/yidaosu1", methods=["GET", "POST"])
def image26():
    with open(r'C:\wechartphoto\yidaosu1.jpg', 'rb') as k:
        image26 = k.read()
        yidaosu1 = Response(image26, mimetype="image/jpg")
        return yidaosu1
@app.route("/muzi/666/koushihuli", methods=["GET", "POST"])
def image27():
    with open(r'C:\wechartphoto\koushihuli.jpg', 'rb') as k:
        image27 = k.read()
        koushihuli = Response(image27, mimetype="image/jpg")
        return koushihuli
@app.route("/muzi/666/bishiyingshi", methods=["GET", "POST"])
def image28():
    with open(r'C:\wechartphoto\bishiyingshi.jpg', 'rb') as k:
        image28 = k.read()
        bishiyingshi = Response(image28, mimetype="image/jpg")
        return bishiyingshi
@app.route("/muzi/666/shiwuxuanze", methods=["GET", "POST"])
def image29():
    with open(r'C:\wechartphoto\shiwuxuanze.jpg', 'rb') as k:
        image29 = k.read()
        shiwuxuanze = Response(image29, mimetype="image/jpg")
        return shiwuxuanze
@app.route("/muzi/666/koushihuli1", methods=["GET", "POST"])
def image30():
    with open(r'C:\wechartphoto\koushihuli1.jpg', 'rb') as k:
        image30 = k.read()
        koushihuli1 = Response(image30, mimetype="image/jpg")
        return koushihuli1
@app.route("/muzi/666/bishiyingshi1", methods=["GET", "POST"])
def image31():
    with open(r'C:\wechartphoto\bishiyingshi1.jpg', 'rb') as k:
        image31 = k.read()
        bishiyingshi1 = Response(image31, mimetype="image/jpg")
        return bishiyingshi1
@app.route("/muzi/666/shiwuxuanze1", methods=["GET", "POST"])
def image32():
    with open(r'C:\wechartphoto\shiwuxuanze1.jpg', 'rb') as k:
        image32 = k.read()
        shiwuxuanze1 = Response(image32, mimetype="image/jpg")
        return shiwuxuanze1
@app.route("/muzi/666/yongyaozhuyi", methods=["GET", "POST"])
def image33():
    with open(r'C:\wechartphoto\yongyaozhuyi.jpg', 'rb') as k:
        image33 = k.read()
        yongyaozhuyi = Response(image33, mimetype="image/jpg")
        return yongyaozhuyi
@app.route("/muzi/666/yinshizhuyi", methods=["GET", "POST"])
def image34():
    with open(r'C:\wechartphoto\yinshizhuyi.jpg', 'rb') as k:
        image34 = k.read()
        yinshizhuyi = Response(image34, mimetype="image/jpg")
        return yinshizhuyi
@app.route("/muzi/666/yundongzhuyi", methods=["GET", "POST"])
def image35():
    with open(r'C:\wechartphoto\yundongzhuyi.jpg', 'rb') as k:
        image35 = k.read()
        yundongzhuyi = Response(image35, mimetype="image/jpg")
        return yundongzhuyi
@app.route("/muzi/666/qingxuzhuyi", methods=["GET", "POST"])
def image36():
    with open(r'C:\wechartphoto\qingxuzhuyi.jpg', 'rb') as k:
        image36 = k.read()
        qingxuzhuyi = Response(image36, mimetype="image/jpg")
        return qingxuzhuyi
@app.route("/muzi/666/yinshizhuyi1", methods=["GET", "POST"])
def image37():
    with open(r'C:\wechartphoto\yinshizhuyi1.jpg', 'rb') as k:
        image37 = k.read()
        yinshizhuyi1 = Response(image37, mimetype="image/jpg")
        return yinshizhuyi1
@app.route("/muzi/666/qingxuzhuyi1", methods=["GET", "POST"])
def image38():
    with open(r'C:\wechartphoto\qingxuzhuyi1.jpg', 'rb') as k:
        image38 = k.read()
        qingxuzhuyi1 = Response(image38, mimetype="image/jpg")
        return qingxuzhuyi1
@app.route("/muzi/666/neikezhiliao", methods=["GET", "POST"])
def image39():
    with open(r'C:\wechartphoto\neikezhiliao.jpg', 'rb') as k:
        image39 = k.read()
        neikezhiliao = Response(image39, mimetype="image/jpg")
        return neikezhiliao
@app.route("/muzi/666/waikezhiliao", methods=["GET", "POST"])
def image40():
    with open(r'C:\wechartphoto\waikezhiliao.jpg', 'rb') as k:
        image40 = k.read()
        waikezhiliao = Response(image40, mimetype="image/jpg")
        return waikezhiliao
@app.route("/muzi/666/kangfu", methods=["GET", "POST"])
def image41():
    with open(r'C:\wechartphoto\kangfu.jpg', 'rb') as k:
        image41 = k.read()
        kangfu = Response(image41, mimetype="image/jpg")
        return kangfu
@app.route("/muzi/666/xueya", methods=["GET", "POST"])
def image42():
    with open(r'C:\wechartphoto\xueya.jpg', 'rb') as k:
        image42 = k.read()
        xueya = Response(image42, mimetype="image/jpg")
        return xueya
@app.route("/muzi/666/xuetang", methods=["GET", "POST"])
def image43():
    with open(r'C:\wechartphoto\xuetang.jpg', 'rb') as k:
        image43 = k.read()
        xuetang = Response(image43, mimetype="image/jpg")
        return xuetang
@app.route("/muzi/666/yaowu", methods=["GET", "POST"])
def image44():
    with open(r'C:\wechartphoto\yaowu.jpg', 'rb') as k:
        image44 = k.read()
        yaowu = Response(image44, mimetype="image/jpg")
        return yaowu
@app.route("/muzi/666/bingyin", methods=["GET", "POST"])
def image45():
    with open(r'C:\wechartphoto\bingyin.jpg', 'rb') as k:
        image45 = k.read()
        bingyin = Response(image45, mimetype="image/jpg")
        return bingyin
@app.route("/muzi/666/qita", methods=["GET", "POST"])
def image46():
    with open(r'C:\wechartphoto\qita.jpg', 'rb') as k:
        image46 = k.read()
        qita = Response(image46, mimetype="image/jpg")
        return qita
@app.route("/muzi/666/bingfa", methods=["GET", "POST"])
def image47():
    with open(r'C:\wechartphoto\bingfa.jpg', 'rb') as k:
        image47 = k.read()
        bingfa = Response(image47, mimetype="image/jpg")
        return bingfa
@app.route("/muzi/666/yiban", methods=["GET", "POST"])
def image48():
    with open(r'C:\wechartphoto\yiban.jpg', 'rb') as k:
        image48 = k.read()
        yiban = Response(image48, mimetype="image/jpg")
        return yiban
@app.route("/muzi/666/xueya1", methods=["GET", "POST"])
def image49():
    with open(r'C:\wechartphoto\xueya1.jpg', 'rb') as k:
        image49 = k.read()
        xueya1 = Response(image49, mimetype="image/jpg")
        return xueya1
@app.route("/muzi/666/xuetang1", methods=["GET", "POST"])
def image50():
    with open(r'C:\wechartphoto\xuetang1.jpg', 'rb') as k:
        image50 = k.read()
        xuetang1 = Response(image50, mimetype="image/jpg")
        return xuetang1
@app.route("/muzi/666/yaowu1", methods=["GET", "POST"])
def image51():
    with open(r'C:\wechartphoto\yaowu1.jpg', 'rb') as k:
        image51 = k.read()
        yaowu1 = Response(image51, mimetype="image/jpg")
        return yaowu1
@app.route("/muzi/666/bingyin1", methods=["GET", "POST"])
def image52():
    with open(r'C:\wechartphoto\bingyin1.jpg', 'rb') as k:
        image52 = k.read()
        bingyin1 = Response(image52, mimetype="image/jpg")
        return bingyin1
@app.route("/muzi/666/qita1", methods=["GET", "POST"])
def image53():
    with open(r'C:\wechartphoto\qita1.jpg', 'rb') as k:
        image53 = k.read()
        qita1 = Response(image53, mimetype="image/jpg")
        return qita1
@app.route("/muzi/666/bingfa1", methods=["GET", "POST"])
def image54():
    with open(r'C:\wechartphoto\bingfa1.jpg', 'rb') as k:
        image54 = k.read()
        bingfa1 = Response(image54, mimetype="image/jpg")
        return bingfa1
@app.route("/muzi/666/yiban1", methods=["GET", "POST"])
def image55():
    with open(r'C:\wechartphoto\yiban1.jpg', 'rb') as k:
        image55 = k.read()
        yiban1 = Response(image55, mimetype="image/jpg")
        return yiban1
@app.route("/muzi/666/naoshi", methods=["GET", "POST"])
def image56():
    with open(r'C:\wechartphoto\naoshi.jpg', 'rb') as k:
        image56 = k.read()
        naoshi = Response(image56, mimetype="image/jpg")
        return naoshi
@app.route("/muzi/666/naosi", methods=["GET", "POST"])
def image57():
    with open(r'C:\wechartphoto\naosi.jpg', 'rb') as k:
        image57 = k.read()
        naosi = Response(image57, mimetype="image/jpg")
        return naosi
@app.route("/muzi/666/naojishui", methods=["GET", "POST"])
def image58():
    with open(r'C:\wechartphoto\naojishui.jpg', 'rb') as k:
        image58 = k.read()
        naojishui = Response(image58, mimetype="image/jpg")
        return naojishui
@app.route("/muzi/666/naoshi1", methods=["GET", "POST"])
def image59():
    with open(r'C:\wechartphoto\naoshi1.jpg', 'rb') as k:
        image59 = k.read()
        naoshi1 = Response(image59, mimetype="image/jpg")
        return naoshi1
@app.route("/muzi/666/naosi1", methods=["GET", "POST"])
def image60():
    with open(r'C:\wechartphoto\naosi1.jpg', 'rb') as k:
        image60 = k.read()
        naosi1 = Response(image60, mimetype="image/jpg")
        return naosi1
@app.route("/muzi/666/naojishui11", methods=["GET", "POST"])
def image61():
    with open(r'C:\wechartphoto\naojishui1.jpg', 'rb') as k:
        image61 = k.read()
        naojishui1 = Response(image61, mimetype="image/jpg")
        return naojishui1
@app.route("/muzi/666/yfff", methods=["GET", "POST"])
def image62():
    with open(r'C:\wechartphoto\yfff.jpg', 'rb') as k:
        image62 = k.read()
        yfff = Response(image62, mimetype="image/jpg")
        return yfff
@app.route("/muzi/666/lclj", methods=["GET", "POST"])
def image63():
    with open(r'C:\wechartphoto\lclj.jpg', 'rb') as k:
        image63 = k.read()
        lclj = Response(image63, mimetype="image/jpg")
        return lclj
@app.route("/muzi/666/yfff1", methods=["GET", "POST"])
def image64():
    with open(r'C:\wechartphoto\yfff1.jpg', 'rb') as k:
        image64 = k.read()
        yfff1 = Response(image64, mimetype="image/jpg")
        return yfff1
@app.route("/muzi/666/lclj1", methods=["GET", "POST"])
def image65():
    with open(r'C:\wechartphoto\lclj1.jpg', 'rb') as k:
        image65 = k.read()
        lclj1 = Response(image65, mimetype="image/jpg")
        return lclj1
@app.route("/muzi/666/test", methods=["GET", "POST"])
def image66():
    with open(r'C:\wechartphoto\test.jpg', 'rb') as k:
        image66 = k.read()
        test = Response(image66, mimetype="image/jpg")
        return test
@app.route("/muzi/666/xuanzrtupian", methods=["GET", "POST"])
def image67():
    with open(r'C:\wechartphoto\选择图片.jpg', 'rb') as k:
        image67 = k.read()
        xuanzrtupian = Response(image67, mimetype="image/jpg")
        return xuanzrtupian
@app.route("/muzi/666/paizhaoshangchuan", methods=["GET", "POST"])
def image68():
    with open(r'C:\wechartphoto\拍照上传.jpg', 'rb') as k:
        image68 = k.read()
        paizhaoshangchuan = Response(image68, mimetype="image/jpg")
        return paizhaoshangchuan
@app.route("/muzi/666/anniu", methods=["GET", "POST"])
def image69():
    with open(r'C:\wechartphoto\按钮.jpg', 'rb') as k:
        image69 = k.read()
        anniu = Response(image69, mimetype="image/jpg")
        return anniu
@app.route("/muzi/666/paizhaoshangmian", methods=["GET", "POST"])
def image70():
    with open(r'C:\wechartphoto\拍照上面.jpg', 'rb') as k:
        image70 = k.read()
        paizhaoshangmian = Response(image70, mimetype="image/jpg")
        return paizhaoshangmian
@app.route("/muzi/666/putongzhengliao", methods=["GET", "POST"])
def image71():
    with open(r'C:\wechartphoto\基础诊疗.jpg', 'rb') as k:
        image71 = k.read()
        putongzhengliao = Response(image71, mimetype="image/jpg")
        return putongzhengliao
@app.route("/muzi/666/zhuanyezhengliao", methods=["GET", "POST"])
def image72():
    with open(r'C:\wechartphoto\专业诊疗.jpg', 'rb') as k:
        image72 = k.read()
        zhuanyezhengliao = Response(image72, mimetype="image/jpg")
        return zhuanyezhengliao
@app.route("/muzi/666/shangchuananniu", methods=["GET", "POST"])
def image73():
    with open(r'C:\wechartphoto\上传按钮.jpg', 'rb') as k:
        image73 = k.read()
        shangchuananniu = Response(image73, mimetype="image/jpg")
        return shangchuananniu
@app.route("/muzi/666/huoquxinxiquantu", methods=["GET", "POST"])
def image74():
    with open(r'C:\wechartphoto\获取信息全图.jpg', 'rb') as k:
        image74 = k.read()
        huoquxinxiquantu = Response(image74, mimetype="image/jpg")
        return huoquxinxiquantu
"""
以下为更新UI的API
"""
@app.route("/muzi/666/mengzhuban", methods=["GET", "POST"])
def image89():
    with open(r'C:\wechartphoto\蒙版组 2.jpg', 'rb') as k:
        image89 = k.read()
        mengzhuban = Response(image89, mimetype="image/jpg")
        return mengzhuban
@app.route("/muzi/666/mengzhuban3", methods=["GET", "POST"])
def image90():
    with open(r'C:\wechartphoto\蒙版组 3.jpg', 'rb') as k:
        image90 = k.read()
        mengzhuban3 = Response(image90, mimetype="image/jpg")
        return mengzhuban3
@app.route("/muzi/666/asd1", methods=["GET", "POST"])
def image91():
    with open(r'C:\wechartphoto\1.jpg', 'rb') as k:
        image91 = k.read()
        asd1 = Response(image91, mimetype="image/jpg")
        return asd1
@app.route("/muzi/666/asd2", methods=["GET", "POST"])
def image92():
    with open(r'C:\wechartphoto\2.jpg', 'rb') as k:
        image92 = k.read()
        asd2 = Response(image92, mimetype="image/jpg")
        return asd2
@app.route("/muzi/666/asd3", methods=["GET", "POST"])
def image93():
    with open(r'C:\wechartphoto\3.jpg', 'rb') as k:
        image93 = k.read()
        asd3 = Response(image93, mimetype="image/jpg")
        return asd3


'''
以下为更新图片的API
'''
@app.route("/muzi/666/baidanbai", methods=["GET", "POST"])
def image75():
    with open(r'C:\wechartphoto\白蛋白.jpg', 'rb') as k:
        image75 = k.read()
        baidanbai = Response(image75, mimetype="image/jpg")
        return baidanbai
@app.route("/muzi/666/ganluchun", methods=["GET", "POST"])
def image76():
    with open(r'C:\wechartphoto\甘露醇.jpg', 'rb') as k:
        image76 = k.read()
        ganluchun = Response(image76, mimetype="image/jpg")
        return ganluchun
@app.route("/muzi/666/ganyou", methods=["GET", "POST"])
def image77():
    with open(r'C:\wechartphoto\甘油.jpg', 'rb') as k:
        image77 = k.read()
        ganyou = Response(image77, mimetype="image/jpg")
        return ganyou
@app.route("/muzi/666/fushaimi", methods=["GET", "POST"])
def image78():
    with open(r'C:\wechartphoto\呋塞米.jpg', 'rb') as k:
        image78 = k.read()
        fushaimi = Response(image78, mimetype="image/jpg")
        return fushaimi
@app.route("/muzi/666/gaoshengyanshui", methods=["GET", "POST"])
def image79():
    with open(r'C:\wechartphoto\高渗盐水.jpg', 'rb') as k:
        image79 = k.read()
        gaoshengyanshui = Response(image79, mimetype="image/jpg")
        return gaoshengyanshui
@app.route("/muzi/666/qingyang", methods=["GET", "POST"])
def image80():
    with open(r'C:\wechartphoto\氢氧噻嗪.jpg', 'rb') as k:
        image80 = k.read()
        qingyang = Response(image80, mimetype="image/jpg")
        return qingyang
@app.route("/muzi/666/baidanbai1", methods=["GET", "POST"])
def image81():
    with open(r'C:\wechartphoto\白蛋白1.jpg', 'rb') as k:
        image81 = k.read()
        baidanbai1 = Response(image81, mimetype="image/jpg")
        return baidanbai1
@app.route("/muzi/666/xiaobengdi", methods=["GET", "POST"])
def image82():
    with open(r'C:\wechartphoto\硝苯地平缓释片.jpg', 'rb') as k:
        image82 = k.read()
        xiaobengdi = Response(image82, mimetype="image/jpg")
        return xiaobengdi
@app.route("/muzi/666/beinapuli", methods=["GET", "POST"])
def image83():
    with open(r'C:\wechartphoto\贝那普利.jpg', 'rb') as k:
        image83 = k.read()
        beinapuli = Response(image83, mimetype="image/jpg")
        return beinapuli

@app.route("/muzi/666/xiaoniuxue", methods=["GET", "POST"])
def image84():
    with open(r'C:\wechartphoto\小牛血去蛋白提取物.jpg', 'rb') as k:
        image84 = k.read()
        xiaoniuxue = Response(image84, mimetype="image/jpg")
        return xiaoniuxue
@app.route("/muzi/666/changchunxiting", methods=["GET", "POST"])
def image85():
    with open(r'C:\wechartphoto\长春西汀.jpg', 'rb') as k:
        image85 = k.read()
        changchunxiting = Response(image85, mimetype="image/jpg")
        return changchunxiting
@app.route("/muzi/666/monidiping", methods=["GET", "POST"])
def image86():
    with open(r'C:\wechartphoto\尼莫地平.jpg', 'rb') as k:
        image86 = k.read()
        monidiping = Response(image86, mimetype="image/jpg")
        return monidiping
@app.route("/muzi/666/yidalafeng", methods=["GET", "POST"])
def image87():
    with open(r'C:\wechartphoto\依达拉奉.jpg', 'rb') as k:
        image87 = k.read()
        yidalafeng = Response(image87, mimetype="image/jpg")
        return yidalafeng
@app.route("/muzi/666/baoerling", methods=["GET", "POST"])
def image88():
    with open(r'C:\wechartphoto\胞二崚胆碱钠.jpg', 'rb') as k:
        image88 = k.read()
        baoerling = Response(image88, mimetype="image/jpg")
        return baoerling
@app.route("/muzi/666/ganchunlu1", methods=["GET", "POST"])
def image94():
    with open(r'C:\wechartphoto\甘露醇1.jpg', 'rb') as k:
        image94 = k.read()
        ganchunlu1 = Response(image94, mimetype="image/jpg")
        return ganchunlu1
@app.route("/muzi/666/ganyou1", methods=["GET", "POST"])
def image95():
    with open(r'C:\wechartphoto\甘油1.jpg', 'rb') as k:
        image95 = k.read()
        ganyou1 = Response(image95, mimetype="image/jpg")
        return ganyou1
@app.route("/muzi/666/fushaimi1", methods=["GET", "POST"])
def image96():
    with open(r'C:\wechartphoto\呋塞米1.jpg', 'rb') as k:
        image96 = k.read()
        fushaimi1 = Response(image96, mimetype="image/jpg")
        return fushaimi1
@app.route("/muzi/666/qingyangshaiqing1", methods=["GET", "POST"])
def image97():
    with open(r'C:\wechartphoto\氢氧噻嗪1.jpg', 'rb') as k:
        image97 = k.read()
        qingyangshaiqing1 = Response(image97, mimetype="image/jpg")
        return qingyangshaiqing1
@app.route("/muzi/666/gaoshenyanshui1", methods=["GET", "POST"])
def image98():
    with open(r'C:\wechartphoto\高渗盐水1.jpg', 'rb') as k:
        image98 = k.read()
        gaoshenyanshui1 = Response(image98, mimetype="image/jpg")
        return gaoshenyanshui1
@app.route("/muzi/666/xiaoniuxue1", methods=["GET", "POST"])
def image99():
    with open(r'C:\wechartphoto\小牛血去蛋白提取物1.jpg', 'rb') as k:
        image99 = k.read()
        xiaoniuxue1 = Response(image99, mimetype="image/jpg")
        return xiaoniuxue1
@app.route("/muzi/666/changchunxiting1", methods=["GET", "POST"])
def image100():
    with open(r'C:\wechartphoto\长春西汀1.jpg', 'rb') as k:
        image100 = k.read()
        changchunxiting1 = Response(image100, mimetype="image/jpg")
        return changchunxiting1
@app.route("/muzi/666/nimodiping1", methods=["GET", "POST"])
def image101():
    with open(r'C:\wechartphoto\尼莫地平1.jpg', 'rb') as k:
        image101 = k.read()
        nimodiping1 = Response(image101, mimetype="image/jpg")
        return nimodiping1
@app.route("/muzi/666/yidalafeng1", methods=["GET", "POST"])
def image102():
    with open(r'C:\wechartphoto\依达拉奉1.jpg', 'rb') as k:
        image102 = k.read()
        yidalafeng1 = Response(image102, mimetype="image/jpg")
        return yidalafeng1
@app.route("/muzi/666/baerling1", methods=["GET", "POST"])
def image103():
    with open(r'C:\wechartphoto\胞二磷胆碱钠1.jpg', 'rb') as k:
        image103 = k.read()
        baerling1 = Response(image103, mimetype="image/jpg")
        return baerling1
@app.route("/muzi/666/jingkouqianghuli2", methods=["GET", "POST"])
def image105():
    with open(r'C:\wechartphoto\经口饮食护理2.jpg', 'rb') as k:
        image105 = k.read()
        jingkouqianghuli2 = Response(image105, mimetype="image/jpg")
        return jingkouqianghuli2
@app.route("/muzi/666/jingkouqianghuli2", methods=["GET", "POST"])
def image106():
    with open(r'C:\wechartphoto\经口饮食护理2.jpg', 'rb') as k:
        image106 = k.read()
        jingkouqianghuli2 = Response(image106, mimetype="image/jpg")
        return jingkouqianghuli2
@app.route("/muzi/666/shiwuxuanze2", methods=["GET", "POST"])
def image107():
    with open(r'C:\wechartphoto\食物选择2.jpg', 'rb') as k:
        image107 = k.read()
        shiwuxuanze2 = Response(image107, mimetype="image/jpg")
        return shiwuxuanze2
@app.route("/muzi/666/yongyaozhuyi2", methods=["GET", "POST"])
def image108():
    with open(r'C:\wechartphoto\用药注意2.jpg', 'rb') as k:
        image108 = k.read()
        yongyaozhuyi2 = Response(image108, mimetype="image/jpg")
        return yongyaozhuyi2
@app.route("/muzi/666/bisiyingshi4", methods=["GET", "POST"])
def image109():
    with open(r'C:\wechartphoto\鼻饲饮食4.jpg', 'rb') as k:
        image109 = k.read()
        bisiyingshi4 = Response(image109, mimetype="image/jpg")
        return bisiyingshi4
@app.route("/muzi/666/naishizhichuxue4", methods=["GET", "POST"])
def image110():
    with open(r'C:\wechartphoto\脑实质出血4.jpg', 'rb') as k:
        image110 = k.read()
        naishizhichuxue4 = Response(image110, mimetype="image/jpg")
        return naishizhichuxue4
@app.route("/muzi/666/yibanzhiliao4", methods=["GET", "POST"])
def image111():
    with open(r'C:\wechartphoto\一般治疗4.jpg', 'rb') as k:
        image111 = k.read()
        yibanzhiliao4 = Response(image111, mimetype="image/jpg")
        return yibanzhiliao4
@app.route("/muzi/666/dianxinfazuo4", methods=["GET", "POST"])
def image112():
    with open(r'C:\wechartphoto\癫痫发作4.jpg', 'rb') as k:
        image112 = k.read()
        dianxinfazuo4 = Response(image112, mimetype="image/jpg")
        return dianxinfazuo4




# 启动路由,访问http://192.168.3.7:5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
