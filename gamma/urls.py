# coding: utf-8

from django.urls import path

from gamma import apis

urlpatterns = [
    path('auth/', apis.AuthView.as_view()),
    path('order/', apis.OrderView.as_view()),
    path('user/', apis.UserView.as_view()),

]

