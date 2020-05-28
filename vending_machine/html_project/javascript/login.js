function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {
    $('#entry_btn').click(function () {

        var username = $('#adminName').val();
        var password = $('#adminPwd').val();


        if (username == '') {
            $('.mask,.dialog').show();
            $('.dialog .dialog-bd p').html('请输入管理员账号');
        } else if (password == '') {
            $('.mask,.dialog').show();
            $('.dialog .dialog-bd p').html('请输入管理员密码');
        } else {
            var param = {
                "username": username,
                "password": password
            }
            $.ajax({
                type: "post",
                url: host + "/api/v1.0/session/",
                contentType: "application/json",
                xhrFields: {
                    withCredentials: true
                },
                data: JSON.stringify(param),
                success: function (resp) {
                    if (resp.code =='ok') {
                        window.sessionStorage.clear();
                        window.localStorage.clear();
                        window.localStorage.setItem('jwt_token',resp.jwt_token);
                        $(location).prop('href', '/index.html')
                    }else{
                        alert(resp.errmsg)
                    }

                },else(){
                    alert('登录超时')
                }

            })
        }
    });
});


$(document).ready(function () {
    window.sessionStorage.clear();
    window.localStorage.clear();
})