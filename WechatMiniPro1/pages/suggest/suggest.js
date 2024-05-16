// pages/suggest/suggest.js
Page({

    /**
     * 页面的初始数据
     */
    //status 数据为获取后端传值的数据
    data: {
status:''
    },

    /**
     * 生命周期函数--监听页面加载
     */
    // get_status函数为点击后向后端地址发送请求
    get_states:function(e){
      var that = this
    wx.request({
      // url为请求的字段
      url: 'https://muzi-03.xyz/get_phone',
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
        // onload;
        // 弹窗功能
        wx.showModal({
          title:'分析报告:',
          content:res.data,
        })
        }
    
    })
    },
    onLoad: function (options) {

    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {

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

    },


      /***
   * 页面跳转
   */

  clickme1: function(){
    wx.navigateTo({
      url: '/pages/food/food',
    })
  },

  clickme2: function(){
    wx.navigateTo({
      url: '/pages/forbid/forbid',
    })
  },

  clickme3: function(){
    wx.navigateTo({
      url: '/pages/heal/heal',
    })
  },

  clickme4: function(){
    wx.navigateTo({
      url: '/pages/medical/medical',
    })
},



})