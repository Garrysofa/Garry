from django.db import models
from django.contrib.auth.models import AbstractUser

# 定义用户模型类
from vending_machine.utils.my_model import BaseModel


class User(AbstractUser):
    email_avtive = models.BooleanField(verbose_name='激活邮箱', default=False)

    class Meta:
        db_table = 'tb_users'


class Facility(models.Model):
    device_code = models.CharField(verbose_name='设备码', max_length=50)
    device_name = models.CharField(verbose_name='设备名称', max_length=20)
    device_address = models.CharField(verbose_name='设备地址', max_length=100)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="设备注册时间")

    class Meta:
        db_table = 'tb_facility'


class DataWeb(models.Model):
    facility_id = models.ForeignKey("Facility", null=False, on_delete=models.CASCADE, verbose_name="设备对应信息")
    last_time = models.DateTimeField(null=False, verbose_name="最后一次连接服务器时间")
    last_ip = models.CharField(verbose_name='连接ip', max_length=20)

    class Meta:
        db_table = 'tb_dataweb'
