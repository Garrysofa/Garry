import re
from django import http
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
import json
from django_redis import get_redis_connection

from users.models import Facility
from vending_machine.utils import constants
from vending_machine.utils.constants import REDIS_MESSAGE_CODE_EXPIRES


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 获取用户参数
        data = json.loads(request.body.decode())
        username = data.get("username")
        pwd = data.get("password")
        # remembered = request.POST.get("remembered")  # 是否勾选记住登录

        if not all([username, pwd]):
            return http.HttpResponseForbidden('用户名或密码未填')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}', username):
            return http.HttpResponseForbidden('用户名格式错误')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}', pwd):
            return http.HttpResponseForbidden('密码格式错误')
        user = authenticate(username=username, password=pwd, request=request)
        if not user:
            return http.HttpResponseForbidden('用户名或密码错误')

        # 保持用户登录状态 是指 lonin(request, user) == request.user = user
        login(request, user)  # 就是将用户的信息存储在session
        # if remembered == "on":
        #     request.session.set_expiry(3600 * 24 * 2)  # 两天
        # else:
        #     request.session.set_expiry(0)  # 一次浏览器会话结束

        # to_url = request.GET.get("redirect_to", "/")
        # response = redirect(to_url)
        # response.set_cookie('username', user.username, max_age=constants.USER_LOGIN_COOKIE_EXPIRES)
        # 合并购物车

        return http.JsonResponse({'errno': '0'})


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


# from vending_machine.utils.my_socket import get_ip


class DeviceView(View):
    def get(self, request):
        all_data = Facility.objects.all()
        my_list = []
        for obj in all_data:
            json_dict = {
                'ip4': obj.device_name,
                'text1': obj.device_num
            }
            my_list.append(json_dict)
        print(my_list)
        return http.JsonResponse({
            'code': 'ok',
            'data': my_list
        })

    def post(self, request):
        data = json.loads(request.body.decode())  # 从web接收要发送的信息
        msg = data.get('msg')
        ip_port = data.get('ip')
        # 校验前端参数 匹配ip：端口 有缺陷
        if not all([msg, ip_port]):
            return http.JsonResponse({'code': 'no', 'errmsg': '输入框不能为空！'})
        if not re.match(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}:[\d]{1,5}$',
                        ip_port):
            str1 = ip_port.split(':')[1]
            try:
                if int(str1[1]) > 65535:
                    return http.JsonResponse({'code': 'no', 'errmsg': '请检查IP地址或者端口'})
            except Exception as e:
                return http.JsonResponse({'code': 'no', 'errmsg': '请检查IP地址或者端口'})

        # 发送给客户端接口 ，通过redis中介 判断设备是否已经上线
        redis_conn = get_redis_connection('default')
        if not redis_conn.exists(ip_port):
            return http.JsonResponse({'code': 'no', 'errmsg': '设备未上线！请检查连接'})

        # 发送信息到redis
        if redis_conn.set(ip_port, msg, REDIS_MESSAGE_CODE_EXPIRES):
            return http.JsonResponse({'code': 'ok', 'errmsg': '发送成功'})
        else:
            return http.JsonResponse({'code': 'ok', 'errmsg': '发送失败，请稍后再试'})
