"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from app import apis

schema_view = get_schema_view(title='Books System API')

urlpatterns = [
    path('admin/', admin.site.urls),

    # 手动原始json 指定content_type
    path('api/v0/publishes/', apis.publish_list_raw),

    # @api_views(['GET', 'POST'])
    path('api/v1/publishes/', apis.publish_list),
    path('api/v1/publish/<int:pk>/', apis.publish_detail),

    # APIView
    path('api/v2/publishes/', apis.PublishList.as_view()),
    path('api/v2/publish/<int:pk>/', apis.PublishDetail.as_view()),

    # Mixin
    path('api/v3/publishes/', apis.ModePublishList.as_view()),
    path('api/v3/publish/<int:pk>/', apis.ModePublishDetail.as_view()),

    # Generics
    path('api/v4/publishes/', apis.GenericPublishList.as_view()),
    path('api/v4/publish/<int:pk>/', apis.GenericPublishDetail.as_view()),


    # ModelSerializer
    path('api/v5/publishes/', apis.ModelPublishList.as_view()),


    # Login
    path('api-auth/', include('rest_framework.urls')),

    # 列出所有的 api 互相关联的api设计 挺好 待测试 ToDo

    # 分页设计

    # 文档
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title='图书管理系统')),

]
