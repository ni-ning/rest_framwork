# coding: utf-8

from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework import exceptions


class MyAuthentication(object):

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
