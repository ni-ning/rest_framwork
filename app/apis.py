# coding: utf-8

from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView, Http404
from rest_framework import mixins, generics
from rest_framework import permissions

from app import models
from app import serializers
from app import permissions as perm


def publish_list_raw(req):
    query_set = models.Publish.objects.all()

    # 字段多时，必须一个一个写
    # data = []
    # for i in query_set:
    #     item = {
    #         'name': i.name,
    #         'city': i.city,
    #         'email': i.email
    #     }
    #
    #     data.append(item)

    data = []
    from django.forms.models import model_to_dict
    for i in query_set:
        data.append(model_to_dict(i))

    # data 为列表对象
    # return HttpResponse(data)

    # json格式的字符串，需要配置content_type
    import json
    return HttpResponse(json.dumps(data), content_type='application/json')

    # Django自带的序列化, data不用json.dumps
    # from django.core import serializers
    # data = serializers.serialize('json', query_set)
    # return HttpResponse(data, content_type='application/json')


@api_view(['GET', 'POST'])
def publish_list(req):

    if req.method == 'GET':
        # 获取出版社列表

        query = models.Publish.objects.all()
        # 序列化多个对象数据 many=True
        s = serializers.PublishSerializer(query, many=True)
        return Response(s.data)

    elif req.method == 'POST':
        # 创建出版社 请求传入的数据 -> 校验 -> 校验成功 -> 保存 -> DB + s.data

        s = serializers.PublishSerializer(data=req.data)
        if s.is_valid():
            # 校验成功
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)
        else:
            # 校验失败
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def publish_detail(req, pk):
    try:
        p = models.Publish.objects.get(pk=pk)
    except models.Publish.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if req.method == 'GET':
        s = serializers.PublishSerializer(p)
        return Response(s.data, status=status.HTTP_200_OK)

    elif req.method == 'PUT':
        s = serializers.PublishSerializer(p, data=req.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    elif req.method == 'DELETE':
        p.delete()
        return Response(status=status.HTTP_200_OK)


class PublishList(APIView):

    def get(self, req):
        query = models.Publish.objects.all()
        # 序列化多个对象数据 many=True
        s = serializers.PublishSerializer(query, many=True)
        return Response(s.data)

    def post(self, req):
        s = serializers.PublishSerializer(data=req.data)
        if s.is_valid():
            # 校验成功
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)
        else:
            # 校验失败
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class PublishDetail(APIView):

    def get_object(self, pk):
        try:
            return models.Publish.objects.get(pk=pk)
        except models.Publish.DoesNotExist:
            raise Http404

    def get(self, req, pk):
        p = self.get_object(pk)
        s = serializers.PublishSerializer(p)
        return Response(s.data, status=status.HTTP_200_OK)

    def put(self, req, pk):
        p = self.get_object(pk)
        s = serializers.PublishSerializer(p, data=req.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, pk):
        p = self.get_object(pk)
        p.delete()
        return Response(status=status.HTTP_200_OK)


class ModePublishList(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):

    queryset = models.Publish.objects.all()
    serializer_class = serializers.PublishSerializer

    def get(self, req, *arg, **kw):
        return self.list(req, *arg, **kw)

    def post(self, req, *arg, **kw):
        return self.create(req, *arg, *kw)


class ModePublishDetail(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):

    queryset = models.Publish.objects.all()
    serializer_class = serializers.PublishSerializer

    def get(self, req, *arg, **kw):
        return self.retrieve(req, *arg, **kw)

    def put(self, req, *arg, **kw):
        return self.update(req, *arg, **kw)

    def delete(self, req, *arg, **kw):
        return self.delete(req, *arg, **kw)


class GenericPublishList(generics.ListCreateAPIView):
    queryset = models.Publish.objects.all()
    serializer_class = serializers.PublishSerializer


class GenericPublishDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Publish.objects.all()
    serializer_class = serializers.PublishSerializer


class ModelPublishList(generics.ListCreateAPIView):

    queryset = models.Publish.objects.all()
    serializer_class = serializers.ModelPublishSerializer

    # 只要满足一个就成立
    # permission_classes = (permissions.IsAuthenticated, perm.MyPermission, )
    permission_classes = (perm.MyPermission, )  # ToDo 待理解

    # # ToDo ???
    # def perform_create(self, serializer):
    #     serializer.save(operator=self.request.user)



