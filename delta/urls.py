# coding: utf-8

from django.urls import path
from rest_framework.routers import DefaultRouter

from delta import apis

"""
自动生成路由
api/v1/ ^books/router/$ [name='books-list']
api/v1/ ^books/router\.(?P<format>[a-z0-9]+)/?$ [name='books-list']
api/v1/ ^books/router/(?P<pk>[^/.]+)/$ [name='books-detail']
api/v1/ ^books/router/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='books-detail']
"""
router = DefaultRouter()
router.register('books/router', apis.BookModelViewSet)


urlpatterns = [
    # 需要指定 method, serializer, model
    path('books/', apis.BookView.as_view()),
    path('books/<int:pk>/', apis.BookDetail.as_view()),

    # 第一次封装：提取公共 serializer, model 手动映射method -> view
    path('books/generic/', apis.BookGenericView.as_view()),
    path('books/generic/<int:pk>/', apis.BookGenericDetail.as_view()),

    # 第二次封装：组合 list create retrieve update destroy
    path('books/lc/', apis.BookListCreate.as_view()),
    path('books/rud/<int:pk>/', apis.BookRetrieveUpdateDestroy.as_view()),

    # 第三次封装：自动映射 method -> view
    path('books/viewset/', apis.BookModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('books/viewset/<int:pk>/', apis.BookModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]

urlpatterns += router.urls
