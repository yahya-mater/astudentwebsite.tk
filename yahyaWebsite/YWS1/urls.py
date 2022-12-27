from django.urls import path
from . import views


app_name = "YWS1"

urlpatterns = [
    path('admin', views.admin, name="admin"),
    path('sub1', views.sub1, name="sub1"),
    path('sub2', views.sub2, name="sub2"),
    path('login', views.login, name="login"),
    path('about', views.about, name="about"),
    path('orders', views.Orders, name="orders"),
    path('orders/<int:id>', views.OrdersDelete, name="ordersDelete"),
    path('logout', views.logout, name="logout"),
    path('signin', views.signin, name="signin"),
    path('test', views.test, name="test")
]