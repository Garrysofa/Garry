from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^api/v1.0/login/$', views.LoginView.as_view()),
    url(r'^api/v1.0/session/$', views.LoginView.as_view()),
    url(r'^api/v1.0/check/$', views.CheckView.as_view()),
    url(r'^api/v1.0/device/$', views.DeviceView.as_view()),
]