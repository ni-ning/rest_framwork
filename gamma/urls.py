# coding: utf-8

from django.urls import path

from gamma import apis

urlpatterns = [
    path('order/', apis.OrderView.as_view()),

]

