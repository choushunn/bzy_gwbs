/*这里是自定义jQuery*/

$(document).ready(function () {

    // 添加动画
    // new WOW().init();
    // $('.art').addClass('wow fadeInDown').attr({
    //     // 'data-wow-duration': '2s',
    //     'data-wow-offset': '20'
    // });
    // $(".fixed-top").headroom({
    //     "tolerance": 5,
    //     "offset": 100,
    //     "classes": {
    //         "initial": "animated",
    //         "pinned": "flipInX",
    //         "unpinned": "flipOutX"
    //     }
    // });
    // 文章列表效果
    // $(".post-hover").mouseover(function () {
    //     $(this).mouseover(function () {
    //         $(this).css("background-color", "#F8F8F8").addClass(['post-border',]);
    //     });
    //     $(this).mouseleave(function () {
    //         $(this).css("background-color", "#fff").removeClass(['post-border',]);
    //     });
    // });

    // 返回顶部
    $.goup({
        trigger: 100,
        bottomOffset: 120,
        locationOffset: 100,
        title: '',
        titleAsText: true
    });

});
