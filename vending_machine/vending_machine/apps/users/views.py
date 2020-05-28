import re
from django import http
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views import View
import json
from django_redis import get_redis_connection
from users.models import Facility, User
from vending_machine.utils import constants
from vending_machine.utils.constants import REDIS_MESSAGE_CODE_EXPIRES
from vending_machine.utils.jwt_authenticate import generate_jwt, verify_jwt


class LoginView(View):
    def post(self, request):
        # 获取用户参数
        data = json.loads(request.body.decode())
        username = data.get("username")
        pwd = data.get("password")
        # remembered = request.POST.get("remembered")  # 是否勾选记住登录
        if not all([username, pwd]):
            return http.JsonResponse({'code': 'no', 'errmsg': '用户名或密码不能为空'})
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}', username):
            return http.JsonResponse({'code': 'no', 'errmsg': '用户名格式有误'})
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}', pwd):
            return http.JsonResponse({'code': 'no', 'errmsg': '密码错误'})
        user = authenticate(request, username=username, password=pwd)
        if not user:
            return http.JsonResponse({"code": 'no', "errmsg": "用户名或密码错误"})

        payload = {"user_id": user.id, "username": user.username}
        jwt_token = generate_jwt(payload)
        return http.JsonResponse({"code": 'ok', "jwt_token": jwt_token})


class CheckView(View):
    def post(self, request):
        # 验证jwt登录
        try:
            jwt_token = request.body.decode()
            payload = verify_jwt(jwt_token)
            if payload:
                user_obj = User.objects.get(id=payload['user_id'])
                return http.JsonResponse({'code': 'ok', 'username': user_obj.username})
            else:
                return http.JsonResponse({'code': 'no', 'errmsg': '请先登录'})
        except:
            return http.JsonResponse({'code': 'no', 'errmsg': '用户验证过期，请重新登录'})


class DeviceView(View):
    def get(self, request):
        all_data = Facility.objects.all()
        my_list = []
        redis_conn = get_redis_connection('is_online')
        for obj in all_data:
            if redis_conn.exists(obj.device_code):
                is_online = '在线'
            else:
                is_online = ' 离线'
            json_dict = {
                'device_code': obj.device_code,
                'device_name': obj.device_name,
                'device_address': obj.device_address,
                'create_time': obj.create_time,
                'is_online': is_online

            }
            my_list.append(json_dict)
        return http.JsonResponse({
            'code': 'ok',
            'data': my_list
        })

    def post(self, request):
        data = json.loads(request.body.decode())  # 从web接收要发送的信息
        msg = data.get('msg')
        ip = data.get('ip')
        print(data)
        # 校验前端参数 匹配ip：端口 有缺陷
        if not all([msg, ip]):
            return http.JsonResponse({'code': 'no', 'errmsg': '输入框不能为空！'})
        if not re.match(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$',
                        ip):
            return http.JsonResponse({'code': 'no', 'errmsg': '请检查IP地址'})
        # 发送给客户端接口 ，通过redis中介 判断设备是否已经上线
        redis_conn = get_redis_connection('is_online')
        if not redis_conn.exists(ip):
            return http.JsonResponse({'code': 'no', 'errmsg': '设备未上线！请检查连接'})

        # 发送信息到redis
        redis_conn = get_redis_connection('send_message')
        if redis_conn.set(ip, msg, REDIS_MESSAGE_CODE_EXPIRES):
            return http.JsonResponse({'code': 'ok', 'errmsg': '发送成功'})
        else:
            return http.JsonResponse({'code': 'no', 'errmsg': '发送失败，请稍后再试'})
