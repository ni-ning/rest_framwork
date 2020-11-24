# coding: utf-8

from django.urls import path

from app import apis

urlpatterns = [
    # 手动原始json 指定content_type
    path('publishes/v0/', apis.publish_list_raw),

    # @api_views(['GET', 'POST'])
    path('publishes/v1/', apis.publish_list),
    path('publish/<int:pk>/v1/', apis.publish_detail),

    # APIView
    path('publishes/v2/', apis.PublishList.as_view()),
    path('publish/<int:pk>/v2/', apis.PublishDetail.as_view()),

    # Mixin
    path('publishes/v3/', apis.ModePublishList.as_view()),
    path('publish/<int:pk>/v3/', apis.ModePublishDetail.as_view()),

    # Generics
    path('publishes/v4/', apis.GenericPublishList.as_view()),
    path('publish/<int:pk>/v4/', apis.GenericPublishDetail.as_view()),

    # ModelSerializer
    path('publishes/v5/', apis.ModelPublishList.as_view()),
]

