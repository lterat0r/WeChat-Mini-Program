
#引入flask、os等包
from flask import Flask, Response, request
import os
import json

app = Flask(__name__)

#定义接口地址为imageprocess
@app.route('/imageprocess', methods=['POST'])
def image_preprocess():
	#获取到post请求传来的file里的image文件
    image = request.files.get("image")
    #获取到post请求里传来的form表单中的文件名字段
    data = request.form.get("filename")

    print(data)
    print(image)
    if image is None:
        return "nothing found"
    #获取到的文件名，将文件存放到对应的位置
    image.save("./photo/"+data+".png")
    return "图片上传成功"

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=8080, debug=True)

