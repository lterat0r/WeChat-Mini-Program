// pages/paizhao2/paizhao2.js
Page({
    /**
     * 页面的初始数据
     */
    data: {
      devicePosition:'back',
      authCamera: false,//用户是否运行授权拍照
    },
    handleCameraError:function() {
      wx.showToast({
        title:'用户拒绝使用摄像头',
        icon: 'none'
      })
    },
    reverseCamera:function(){
      this.setData({
        devicePosition: "back" === this.data.devicePosition ? "front" : "back"
    });
    },
    takePhoto:function() {
      //拍摄照片
      let _this = this;
      wx.createCameraContext().takePhoto({
        quality: 'high',//拍摄质量(high:高质量 normal:普通质量 low:高质量)
        success: (res) => {
          //拍摄成功
          //照片文件的临时文件
          var file = res.tempImagePath;
          console.log(file)
          //上传图片到服务器
          wx.uploadFile({
            url: 'https://muzi-03.xyz/uploader5', //上传服务器地址
            filePath: file,
            name: 'file',
            formData: {
              'test': 'test'
            },
            success: (res) => {
              let _data = res.data;
              if (typeof _data == "string") {
                _data = JSON.parse(_data);
                console.log(res);
              }
              getApp().globalData.filename = _data.data
              _this.setData({
                filename: _data.data,
              });
              //上传成功
              wx.showToast({
                title: '上传成功', //弹框内容
                icon: 'fail', //弹框模式
                duration: 2000 //弹框显示时间
              })
              setTimeout(()=>{
                wx.navigateBack({
                  delta: 1 //返回上一级页面
                })
              },2000)
            },
            fail: function(t) {
              //上传失败
            },
          })
        },
        fail: (res) => {
          //拍摄失败
        },
        
      })
  
    },
    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {
      wx.getSetting({
        success: (res) => {
            if (res.authSetting["scope.camera"]) {
                this.setData({
                  authCamera:true,
                })
            } else {
              this.setData({
                authCamera:false,
              })
            }
        }
      });
    },


    /**
   * 获取体积信息
   */
  getAreaData(callback) {
    let _this = this;
    wx.request({
      url: "https://muzi-03.xyz/getdata/" + getApp().globalData.filename,
      method: "GET",
      header: {
        "content-type": "application/json", // 默认值
      },
      success(res) {
        let _data = res.data;
        console.log(_data)
        if (typeof _data == "string") {
          _data = JSON.parse(_data);
        }
        _this.setData({
          mjList: _data.data,
        });
        if (callback) callback(_data.data);
      },
    });
  },
 
  })