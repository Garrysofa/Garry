from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# 加载项目环境
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vending_machine.settings.dev')

# 创建celery对象
app = Celery('proj')
# 加载配置
app.config_from_object('celery_tasks.config', namespace='CELERY')
# 自动注册任务
app.autodiscover_tasks(['celery_tasks.tcp_server'])


# @app.task(bind=True)
# def debug_task(self):
#     print('任务一正在运行')

#  celery -A celery_ worker -l info
