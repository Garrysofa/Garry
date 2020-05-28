from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^api/v1.0/session/$', views.LoginView.as_view()),
    url(r'^api/v1.0/check/$', views.CheckView.as_view()),
    url(r'^api/v1.0/device/$', views.DeviceView.as_view()),
]