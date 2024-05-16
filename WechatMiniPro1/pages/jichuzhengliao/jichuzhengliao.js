// pages/index/index.js
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
      status:''
    },
  
      /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {
      let _this = this;
      _this.setData({
        mjList: []
      });
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
          "https://muzi-03.xyz/uploader/%3Cimage%3E.jpg" +
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
  
   /* takePhoto: function () {
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
  */
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
          getApp().globalData.filename = _data.data
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
      const t=this
      const status=t.data.status
      if(status=='第一级：一级脑出血者一般没有明显症状或仅有轻度头痛和颈强直的情况，一般不需要治疗，但应避免情绪波动，戒烟戒酒。'){
        wx.navigateTo({
          url: '../analyze/pageOne/pageOne',
        })
      }
      if(status=='第二级：二级脑出血者可能会出现头痛或一侧肢体明显瘫痪的现象，容易导致运动能力下降及感觉异常。可使用阿司匹林片、丁苯酞软胶囊、对乙酰氨基酚片等药物缓解症状。'){
        wx.navigateTo({
          url: '../analyze/pageTwo/pageTwo',
        })
      }
      if(status=='第三级：三级脑出血者可能会出现轻度意识障碍，烦躁不安等症状。可在医生建议下使用药物再配合高压氧、理疗、针灸的方式治疗，促使脑功能恢复。'){
        wx.navigateTo({
          url: '../analyze/pageThree/pageThree',
        })
      }
      if(status=='第四级：四级脑出血者可能会出现浅昏迷、偏侧肢体瘫痪、大脑强直和植物神经功能障碍的症状。一般需要通过去骨瓣减压术、小骨窗开颅血肿清除术、钻孔穿刺血肿碎吸术、内镜血肿清除术等手术方式治疗。同时还要注意术后护理，避免辛辣、刺激性食物'){
        wx.navigateTo({
          url: '../analyze/pageFour/pageFour',
        })
      }
      if(status=='第五级：五级脑出血者一般会出现深度昏迷的症状，应及时去医院就诊以免延误时间危及生命，配合医生积极治疗。同时还要注意饮食，多吃富含膳食纤维的食物，如红薯、西蓝花、蘑菇等'){
        wx.navigateTo({
          url: '../analyze/pageFive/pageFive',
        })
      }
      
      // wx.navigateTo({
      //   url: "/pages/suggest/suggest",
      // });
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
        //onload;
        // 弹窗功能
        wx.showModal({
          title:'分析报告:',
          content:that.data.status,
        })
        }
    
    })
    },
  
      aaa: function(){
      wx.navigateTo({
        url: '../paizhaoxuanze/paizhaoxuanze',
      })
      },
  });
  