# coding: utf-8

from django.urls import path

from delta import apis

urlpatterns = [
    path('books/', apis.BookView.as_view()),
    path('books/<int:pk>/', apis.BookDetail.as_view()),
]
