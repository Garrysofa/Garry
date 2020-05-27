from django.conf import settings
from django.core.mail import send_mail
from celery_tasks.celery import app


@app.task(bind=True)
def send_verify_email(self, verify_url, email):
    result = -1
    try:
        result = send_mail(subject="美多商城", message=verify_url, recipient_list=[email], from_email=settings.EMAIL_FROM)
    except Exception as e:
        print(e)
        result = -1

    # 2,判断是否发送成功
    if result != 1:
        # 重试, exc: 发送邮件失败报的异常,  countdown: 间隔几秒重试, max_retries:重试的次数
        self.retry(exc=Exception("发送邮件失败"), countdown=5, max_retries=3)


if __name__ == '__main__':
    result = send_mail(subject="美多商城", message="....", recipient_list=["1127032519@qq.com"],
                       from_email='美多商城<garrysoufa@163.com>')
