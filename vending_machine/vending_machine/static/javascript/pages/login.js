$(function(){
	$('#entry_btn').click(function(){

		var username=$('#adminName').val();
		var password=$('#adminPwd').val();


		if(username==''){
			$('.mask,.dialog').show();
			$('.dialog .dialog-bd p').html('请输入管理员账号');
		}else if(password==''){
			$('.mask,.dialog').show();
			$('.dialog .dialog-bd p').html('请输入管理员密码');
		}else{
			var param= {
					"username":username,
					"password": password
			}
			$.ajax({
				type: "post",
				url: "http://127.0.0.1:8000/login/",
                contentType: "application/json",
                xhrFields: {
                    withCredentials: true
                },
                data : JSON.stringify(param),
				success:  function (resp) {
                    if (resp.errno == "0") {
                        // 跳转到首页
                        location.href = "http://127.0.0.1:8000/"
                    }
                    else {
						console.log('校验失败')
					}
				},

			})
		}
	});
});
