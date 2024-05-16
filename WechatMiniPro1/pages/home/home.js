// pages/home/home.js

var app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: null
  },


  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    //本地storage中获取值
    // this.setData({
    //   userInfo: app.globalData.userInfo
    // })
  },
   /**
   * 用户注销
   */
  onClickLogout:function(){
    app.delUserInfo();
    this.setData({
      userInfo: null
    })
  },
  login(){
    const that = this
    wx.getUserProfile({
        desc: '获取你的昵称、头像、地区及性别',
        success: function (res) {
            console.log(res)
            wx.showToast({
              title: "登录成功\n再次点击以注销",
              icon: "none"
            })
            that.setData({
                userInfo:res.userInfo
            })
        }
    }) 
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})