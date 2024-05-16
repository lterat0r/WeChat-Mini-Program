// pages/VIP2/VIP2.js
Page({
    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {
      // 显示顶部刷新图标
      wx.showNavigationBarLoading();
      //关闭当前非tabbar页面，跳转到应用内的某个页面
      //如果不行使用wx.reLaunch，关闭所有页面，打开到应用内的某个页面
      wx.redirectTo({
        //加载页面地址
        url: "/pages/index/index",
        success: function (_res) {
          // 隐藏导航栏加载框
          wx.hideNavigationBarLoading();
          // 停止下拉动作
          wx.stopPullDownRefresh();
        },
      });
    },
  
    /**
     * 页面的初始数据
     */
    data: {
      filename: "",
      mjList: [],
    },
    //添加Banner 
    chooseImage: function () {
        let _this = this;
        wx.chooseImage({
          count: 6,
          sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
          sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
          success(res) {
            // tempFilePath可以作为img标签的src属性显示图片
            const tempFilePaths = res.tempFilePaths
            for (let i = 0; i < tempFilePaths.length; i += 1) {
              wx.uploadFile({
                url: 'https://muzi-03.xyz/uploader1', //仅为示例，非真实的接口地址
                filePath: tempFilePaths[i],
                name: 'file',
                header: { // 我的 HTTP 请求中需要token，视情况而定是否需要header
                  token: wx.getStorageSync('token') || '',
                },
                formData: { // HTTP 请求中其他额外的 form data
                  file: tempFilePaths[i],
                },
                success: function (res) {
                  let _data = res.data;
                  if (typeof _data == "string") {
                    _data = JSON.parse(_data);
                    console.log(res);
                  }
                  getApp().globalData.filename = _data.data
                  _this.setData({
                    filename: _data.data,
                  });
                  // setTimeout(() => {
                  //   _this.getAreaData();
                  // }, 1000);
                  // 上传成功后相关操作
                  wx.showToast({
                    title: '上传成功', //弹框内容
                    icon: 'fail', //弹框模式
                    duration: 2000 //弹框显示时间
                  })
                  
                },
                fail: function (res) {
                  wx.showToast({
                    title: '上传失败，请重试', //弹框内容
                    icon: 'fail', //弹框模式
                    duration: 2000 //弹框显示时间
                  })
                  
                },
              })
            }
          },
        })
        
    
    
      },
   //添加Banner 
    chooseImage1: function () {
        let _this = this;
        wx.chooseImage({
          count: 6,
          sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
          sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
          success(res) {
            // tempFilePath可以作为img标签的src属性显示图片
            const tempFilePaths = res.tempFilePaths
            for (let i = 0; i < tempFilePaths.length; i += 1) {
              wx.uploadFile({
                url: 'https://muzi-03.xyz/uploader2', //仅为示例，非真实的接口地址
                filePath: tempFilePaths[i],
                name: 'file',
                header: { // 我的 HTTP 请求中需要token，视情况而定是否需要header
                  token: wx.getStorageSync('token') || '',
                },
                formData: { // HTTP 请求中其他额外的 form data
                  file: tempFilePaths[i],
                },
                success: function (res) {
                  let _data = res.data;
                  if (typeof _data == "string") {
                    _data = JSON.parse(_data);
                    console.log(res);
                  }
                  getApp().globalData.filename = _data.data
                  _this.setData({
                    filename: _data.data,
                  });
                  // setTimeout(() => {
                  //   _this.getAreaData();
                  // }, 1000);
                  // 上传成功后相关操作
                  wx.showToast({
                    title: '上传成功', //弹框内容
                    icon: 'fail', //弹框模式
                    duration: 2000 //弹框显示时间
                  })
                  
                },
                fail: function (res) {
                  wx.showToast({
                    title: '上传失败，请重试', //弹框内容
                    icon: 'fail', //弹框模式
                    duration: 2000 //弹框显示时间
                  })
                  
                },
              })
            }
          },
        })
        
    
    
      },
    
    reLoadImage: function (event) {
      console.log(event);
      wx.removeStorage({
        key: "tupian:",
        success(res) {
          console.log(res);
        },
      });
      this.setData({
        tupian:
          "https://muzi-03.xyz/uploader1/%3Cimage%3E.jpg" +
          "?" +
          Math.random(),
      });
      if (this.data.mjList.length <= 0) {
        this.getAreaData((data) => {
          wx.showModal({
            title: "提示",
            content: JSON.stringify(data),
            success: function (res) {},
          });
        });
      } else {
        wx.showModal({
          title: "提示",
          content: JSON.stringify(this.data.mjList),
          success: function (res) {},
        });
      }
    },
    /**
     *  点击绑定的事件
     */
    takePhoto: function () {
      let _this = this;
      wx.chooseImage({
        success(res) {
          const tempFilePaths = res.tempFilePaths;
          wx.showToast({
            title: "选择成功，请稍等",
            duration: 1500,
          });
  
          console.log(tempFilePaths[0]);
          wx.uploadFile({
            //你的后端api地址
            url: "https://muzi-03.xyz/uploader",
            filePath: tempFilePaths[0],
            name: "file",
            formData: {
              user: "test",
            },
            success: function (res) {
              let _data = res.data;
              if (typeof _data == "string") {
                _data = JSON.parse(_data);
              }
              _this.setData({
                filename: _data.data,
              });
              setTimeout(() => {
                _this.getAreaData();
              }, 1000);
            },
            fail: function (res) {
              wx.showModal({
                title: "提示",
                content: "抱歉，服务器暂未开通服务",
                success: function (res) {
                  if (res.confirm) {
                    //这里是点击了确定以后
                    console.log("用户点击确定");
                  } else {
                    //这里是点击了取消以后
                    console.log("用户点击取消");
                  }
                },
              });
              console.log("取消", res.errMsg);
            },
          });
        },
      });
    },
  
    takePhoto1: function () {
      let _this = this;
      wx.chooseImage({
        success(res) {
          const tempFilePaths = res.tempFilePaths;
          wx.showToast({
            title: "选择成功，请稍等",
            duration: 1500,
          });
  
          console.log(tempFilePaths[0]);
          wx.uploadFile({
            //你的后端api地址
            url: "https://muzi-03.xyz/uploader1",
            filePath: tempFilePaths[0],
            name: "file",
            formData: {
              user: "test",
            },
            success: function (res) {
              let _data = res.data;
              if (typeof _data == "string") {
                _data = JSON.parse(_data);
              }
              _this.setData({
                filename: _data.data,
              });
              setTimeout(() => {
                _this.getAreaData();
              }, 1000);
            },
            fail: function (res) {
              wx.showModal({
                title: "提示",
                content: "抱歉，服务器暂未开通服务",
                success: function (res) {
                  if (res.confirm) {
                    //这里是点击了确定以后
                    console.log("用户点击确定");
                  } else {
                    //这里是点击了取消以后
                    console.log("用户点击取消");
                  }
                },
              });
              console.log("取消", res.errMsg);
            },
          });
        },
      });
    },
  
    takePhoto2: function () {
      let _this = this;
      wx.chooseImage({
        success(res) {
          const tempFilePaths = res.tempFilePaths;
          wx.showToast({
            title: "选择成功，请稍等",
            duration: 1500,
          });
  
          console.log(tempFilePaths[0]);
          wx.uploadFile({
            //你的后端api地址
            url: "https://muzi-03.xyz/uploader2",
            filePath: tempFilePaths[0],
            name: "file",
            formData: {
              user: "test",
            },
            success: function (res) {
              let _data = res.data;
              if (typeof _data == "string") {
                _data = JSON.parse(_data);
              }
              _this.setData({
                filename: _data.data,
              });
              setTimeout(() => {
                _this.getAreaData();
              }, 1000);
            },
            fail: function (res) {
              wx.showModal({
                title: "提示",
                content: "抱歉，服务器暂未开通服务",
                success: function (res) {
                  if (res.confirm) {
                    //这里是点击了确定以后
                    console.log("用户点击确定");
                  } else {
                    //这里是点击了取消以后
                    console.log("用户点击取消");
                  }
                },
              });
              console.log("取消", res.errMsg);
            },
          });
        },
      });
    },
    /**
     * 获取体积信息
     */
    getAreaData(callback) {
      let _this = this;
      wx.request({
        url: "https://muzi-03.xyz/getdata/" + this.data.filename,
        method: "GET",
        header: {
          "content-type": "application/json", // 默认值
        },
        success(res) {
          let _data = res.data;
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
  
    /***
     * 页面跳转
     */
    clickme1: function () {
      wx.navigateTo({
        url: "/pages/suggest/suggest",
      });
    },
  
    clickme2: function () {
      wx.navigateTo({
        url: "/pages/VIP/VIP",
      });
    },
  
    // get_status函数为点击后向后端地址发送请求
    get_states1:function(e){
      var that = this
    wx.request({
      // url为请求的字段
      url: 'https://muzi-03.xyz/get_phone1',
      // 请求方法为POST
      method:'POST',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
    // 请求成功后执行以下函数
      success: function (res) {
    
        console.log(res.data); //控制台输出返回数据
        // that.setdata为获取到了后端的数据后将数据传回到小程序的data当中
        that.setData({
          status:res.data
        })
        onload;
        // 弹窗功能
        wx.showModal({
          title:'分析报告:',
          content:that.data.status,
  
        })
        }
    
    })
    },
    onLoad: function (options) {
  
    },
    clickme3: function () {
        wx.navigateTo({
          url: "/pages/paizhaoxuanze1/paizhaoxuanze1",
        });
    },
    clickme4: function () {
      wx.navigateTo({
        url: "/pages/paizhaoxuanze2/paizhaoxuanze2",
      });
    },
  });
  