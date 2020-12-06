# coding: utf-8

import json
import hashlib
import time

from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.versioning import BaseVersioning, QueryParameterVersioning
from rest_framework.parsers import JSONParser, FormParser, FileUploadParser

from gamma import models
from gamma import serializers


# 推荐继承 BaseAuthentication
class MyAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.query_params.get('token')
        if not token:
            raise exceptions.AuthenticationFailed('not token')

        return 'linda', None

    def authenticate_header(self, value):
        pass


class OrderView(APIView):
    authentication_classes = [MyAuthentication, ]

    def get(self, request):
        # APIView重构分发
        self.dispatch

        # 不在是 django 原有的 request，进行加工丰富了
        print(request)

        return HttpResponse('GET: %s' % request.user)


class AuthView(APIView):

    def post(self, request):
        """
        用户注册模拟
        输入：POST form data
        输出：from django.http import JsonResponse
        """
        ret = {
            'code': 1000,
            'msg': None
        }

        username = request._request.POST.get('username')
        password = request._request.POST.get('password')
        user = models.UserInfo.objects.filter(username=username, password=password).first()
        if not user:
            ret['code'] = 1001
            ret['msg'] = '用户名或密码错误'
            return JsonResponse(ret)

        # 为登录用户创建token
        token = self.md5(username)
        # 存在就更新，不存在就创建 - ** token更新 **
        models.UserToken.objects.update_or_create(user=user, defaults={'token': token})
        # 返回 token
        ret['token'] = token
        return JsonResponse(ret)

    @staticmethod
    def md5(plain):
        # hash 需要bytes, now为盐
        now = str(time.time())
        m = hashlib.md5(bytes(plain, encoding='utf-8'))
        m.update(bytes(now, encoding='utf-8'))
        return m.hexdigest()


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):

        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()

        if not token_obj:
            # 内部会捕捉这个异常 status_code=403 Forbidden
            raise exceptions.AuthenticationFailed('用户认证失败')

        # 在rest_framework内部会将这两个字段赋值给request, 以供后续操作使用
        # request.user, request.auth
        return token_obj.user, token_obj

    def authenticate_header(self, value):
        pass


class UserView(APIView):

    # 认证通过时 request.user request.auth
    # Django 全局配置 ToDo
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        """
        获取用户基本信息，必须登录

        谁带着有效的token来，就映射为谁
        """

        # 这种写法需要每个 Method URL都要验证，代码重复，可以借助 DRF 提供的初始化钩子验证
        # token = request._request.GET.get('token')
        # if not token:
        #     return JsonResponse({'code': 1002, 'msg': '用户未登录'})

        print(request.user)
        print(request.auth)

        ret = {
            'code': 1000,
            'msg': None,
            'data': {
                'id': 1,
                'nickname': 'lightnning'
            }
        }
        return JsonResponse(ret)


class ParamVersioning(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get('ver')
        return version


class UsersView(APIView):

    # 可以再view中解析request，也可以利用钩子，自定义类 自动处理
    # versioning_class = ParamVersioning
    versioning_class = QueryParameterVersioning

    def get(self, request):

        self.dispatch
        # request.attr 没有时 会代理到 _reqeust
        # version = request.query_params.get('version')

        # 获取版本
        print(request.version)
        # 获取处理版本的对象
        print(request.versioning_scheme)
        # 根据viewname反向生成url 赞
        u1 = request.versioning_scheme.reverse('uuu', request=request)
        print(u1)

        from django.urls import reverse
        u2 = reverse(viewname='uuu')
        print(u2)

        return HttpResponse('用户列表')


class DjangoView(APIView):

    def post(self, request):

        print(type(request._request))

        from django.core.handlers.wsgi import WSGIRequest

        return HttpResponse('django.request.body')


class ParserView(APIView):
    parser_classes = [JSONParser, FormParser]

    """
    JSONParser: 表示只能解析 content-type: application/json头
    FormParser: 表示只能接卸 content-type: x-www-form-urlencoded头
    """

    def post(self, request):

        print(request.data)
        """
        1. 获取用户请求
        2. 获取用户请求体
        3. 根据请求头 和 parser_classes = [JSONParser, FormParser] 中支持的请求头进行比较
        4. 让JSONParser对象 解析 请求体
        5. 解析结果 得到 request.data
        """
        return HttpResponse('OK')


class RoleView(APIView):
    def get(self, request):
        # 方式一：原始json
        # query_set = models.Role.objects.all().values('id', 'title')
        # roles = list(query_set)
        # ret = json.dumps(roles, ensure_ascii=False)

        # 方式二：多个 [obj, obj, obj]
        # query_set = models.Role.objects.all()
        # ser = serializers.RoleSerializer(instance=query_set, many=True)
        # # 有序字典
        # ret = json.dumps(ser.data)

        # 方式三: 单个 obj
        role = models.Role.objects.all().first()
        ser = serializers.RoleSerializer(instance=role, many=False)
        ret = json.dumps(ser.data)
        return HttpResponse(ret)


class UserInfoView(APIView):
    def get(self, request):

        query_set = models.UserInfo.objects.all()

        # 方式一：自定义序列化字段
        # ser = serializers.UserInfoSerializer(instance=query_set, many=True)

        # 方式二：自定义 ModelSerializer
        ser = serializers.UserInfoModelSerializer(instance=query_set, many=True)

        ret = json.dumps(ser.data)
        return HttpResponse(ret)
