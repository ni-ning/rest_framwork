# coding: utf-8

from django.urls import path

from gamma import apis

urlpatterns = [
    path('auth/', apis.AuthView.as_view()),
    path('order/', apis.OrderView.as_view()),
    path('user/', apis.UserView.as_view()),

    path('users/', apis.UsersView.as_view(), name='uuu'),   # 版本 version
    path('django/', apis.DjangoView.as_view()),             # Django自带解析
    path('parser/', apis.ParserView.as_view()),             # DRF解析规则
    path('roles/', apis.RoleView.as_view()),                # 基本序列化
    path('userinfo/', apis.UserInfoView.as_view()),         # 复杂序列化

]

