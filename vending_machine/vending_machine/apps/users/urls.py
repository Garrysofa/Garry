from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^$', views.HomeView.as_view()),
    url(r'^api/v1.0/device/$', views.DeviceView.as_view()),
]