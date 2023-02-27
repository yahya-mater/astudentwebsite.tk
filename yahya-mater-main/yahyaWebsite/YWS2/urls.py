from django.urls import path
from . import views


app_name = "YWS2"

urlpatterns = [
    path('log-in', views.log_in, name="log-in"),
    path('sign-in', views.sign_in, name="sign-in"),
    path('log-out', views.log_out, name="log-out"),
    path('setting', views.setting, name="setting"),
]