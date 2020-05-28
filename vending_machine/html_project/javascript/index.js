



$(document).ready(function () {
    
    var str1 = '';
    var str2 = '';
    var jwt = localStorage.getItem('jwt_token');
    // 检查用户的登录状态
    $.ajax({
        url: host + '/api/v1.0/check/',
        type: "post",
        contentType: "application/json",
        data: jwt,
        // xhrFields: {withCredentials: true},
        success: function (resp) {
            if (resp.code == "ok"){
                str1 = '<em>' +resp.username+ '</em>';
                $("#username").html(str1);

                }else {
                    // 没有登录
                    alert(resp.errmsg)
                    location.href = "/login.html"

                }
            },else(){
                alert('连接超时')
            }
        
        })

    $.ajax({
        type: "get",
        url: host + '/api/v1.0/device/',
        contentType: "application/json",
        xhrFields: {withCredentials: true},
        // data : JSON.stringify(param),
        success: function (resp) {
            if (resp.code == 'ok') {
                $.each(resp.data, function (index, values) {   // 解析出data对应的Object数组
                    // console.log('可以输出'+ values.ip4 + "  " + values.text1);
                    str1 += '<tr class="cen">';
                    str1 += '<td ><b>' + values.device_code + '</b></td>';
                    str1 += '<td ><b>' + values.device_name + '</b></td>';
                    str1 += '<td><b>' + values.device_address + '</b></td>';
                    str1 += '<td><b>' + values.create_time + '</b></td>';
                    str1 += '<td ><b class="text-warning">' + values.is_online + '</b></td></tr>';
                    if ( values.is_online == '在线') {
                        str2 += '<option>' + values.device_code + '</option>';
                        }


                });
                $("#select_id").html(str2);
                $("#PRO_UL").html(str1);
            }
            else {
                alert('服务器未返回信息')
            }
        }
    })

})


$(document).on('click', "#my", function () {
    var str = $('.fname').val();
    var str1 = $('#select_value option:selected').val();
    params = {"ip": str1, "msg": str};
    $.ajax({
        type: 'post',
        url: host + '/api/v1.0/device/',
        data:JSON.stringify(params),
        cache: false,
        dataType: 'json',
        contentType: "application/json",
        xhrFields: {withCredentials: true},
        success: function (resp) {
            if (resp.code == 'ok') {
                alert('发送成功')
            }
            else {
                alert(resp.errmsg)
            }
        }
    });
})



