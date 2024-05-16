// pages/shangchuan/shangchuan.js
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
      url: "/pages/paizhaoxuanze/paizhaoxuanze",
      success: function (_res) {
        // 隐藏导航栏加载框
        wx.hideNavigationBarLoading();
        // 停止下拉动作
        wx.stopPullDownRefresh();
      },
    });
  },
  data: {

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
            url: 'https://muzi-03.xyz/uploader', //仅为示例，非真实的接口地址
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
              setTimeout(()=>{
                wx.navigateBack({
                  delta: 1 //返回上一级页面
                })
              },2000)
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
  paizhao: function () {
    wx.navigateTo({
      url: '../paizhao/paizhao',
    })
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
        if (typeof _data == "string") {
          _data = JSON.parse(_data);
        }
        getApp().globalData.mjList = _data.data
        _this.setData({
          mjList: _data.data,
        });
        if (callback) callback(_data.data);
      },
    });
  },

})