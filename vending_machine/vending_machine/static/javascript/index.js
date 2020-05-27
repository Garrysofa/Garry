// $(document).ready(function () {
//     // 检查用户的登录状态
//     $.ajax({
//         type: "get",
//         url: 'http://127.0.0.1:8000/api/v1.0/device/',
//         contentType: "application/json",
//         xhrFields: {withCredentials: true},
//         // data : JSON.stringify(param),
//         success: function (resp) {
//             if (resp.errmsg == 'ok') {
//                 alert(resp.ip4)
//                 alert(resp.text1)
//                 $('.ip').html(resp.ip4);
//                 $(".text").html(resp.text1);
//             }
//             else {
//                 alert('服务器未返回信息')
//             }
//         }
//     })
// })



$(document).ready(function () {
    // 检查用户的登录状态
    $.ajax({
        type: "get",
        url: host + '/api/v1.0/device/',
        contentType: "application/json",
        xhrFields: {withCredentials: true},
        // data : JSON.stringify(param),
        success: function (resp) {
            if (resp.code == 'ok') {
                console.log(resp.data)
                var str1;
                $.each(resp.data, function(index,values){   // 解析出data对应的Object数组
                    // console.log('可以输出'+ values.ip4 + "  " + values.text1);
                    str1 += '<tr class="cen">';
					str1 +=	'<td ><b>' + values.ip4 + '</b></td>';
					str1 +=	'<td ><b>' + values.text1 + '</b></td>';
					str1 +=	'<td><b>还没做</b></td>';
					str1 +=	'<td><b class="text-warning">还没做</b></td></tr>';

                });
                console.log(str1)
                $("#PRO_UL").html(str1);
            }
            else {
                alert('服务器未返回信息')
            }
        }
    })
})


$(document).on('click',".my",function(){
    var str = $('.fname').val();
    $.ajax({
        type:'post',
        url:'http://127.0.0.1:8000/api/v1.0/device/',
        data: str,
        cache:false,
        dataType:'json',
        contentType: "application/json",
        xhrFields: {withCredentials: true},
        success:function(data){
            if (resp.errmsg == 'ok') {
                alert('信息上传成功')
            }
            else {
                alert('服务器未返回信息')
            }
        }
    });
})


