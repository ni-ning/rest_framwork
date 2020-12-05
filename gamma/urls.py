# coding: utf-8

from django.urls import path

from gamma import apis

urlpatterns = [
    path('auth/', apis.AuthView.as_view()),
    path('order/', apis.OrderView.as_view()),
    path('user/', apis.UserView.as_view()),

    path('users/', apis.UsersView.as_view(), name='uuu'),   # 版本 version
    path('django/', apis.DjangoView.as_view()),
    path('parser/', apis.ParserView.as_view()),

]

