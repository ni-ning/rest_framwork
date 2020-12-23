# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response

from delta import models
from delta import serializers


# APIView 手动分发
class BookView(APIView):
    """
    Note that we strongly restrict the ordering of operations/properties
    that may be used on the serializer in order to enforce correct usage.

    In particular, if a `data=` argument is passed then:

    .is_valid() - Available.
    .initial_data - Available.
    .validated_data - Only available after calling `is_valid()`
    .errors - Only available after calling `is_valid()`
    .data - Only available after calling `is_valid()`

    If a `data=` argument is not passed then:

    .is_valid() - Not available.
    .initial_data - Not available.
    .validated_data - Not available.
    .errors - Not available.
    .data - Available.
    """

    def get(self, request, *arg, **kw):
        """
        获取列表
        """
        query_set = models.Books.objects.all()
        # 序列化器 作用一: 序列化对象，多个
        book_ser = serializers.BookSerializer(query_set, many=True)
        # 序列化器 结果 book_ser.data
        return Response(book_ser.data)

    def post(self, request, *arg, **kw):
        """
        创建记录
        """
        # 序列化器 作用二: 创建时校验数据，注意传入的参数
        book_ser = serializers.BookSerializer(data=request.data)

        # 执行校验
        if book_ser.is_valid():
            # 校验后创建记录
            book_ser.save()     # 执行self.create
            return Response(book_ser.validated_data)    # 校验成功数据
        else:
            return Response(book_ser.errors)            # 校验异常数据


class BookDetail(APIView):
    def get(self, request, pk, *arg, **kw):
        """
        获取详情
        """
        query_set = models.Books.objects.filter(id=pk).first()
        # 序列化器 作用一: 序列化对象, 单个
        book_ser = serializers.BookSerializer(query_set)
        # 序列化器 结果 book_ser.data
        return Response(book_ser.data)

    def put(self, request, pk,  *arg, **kw):
        """
        更新记录
        """
        query_set = models.Books.objects.filter(id=pk).first()
        # 序列化器 作用二: 更新时校验数据，注意传入的参数
        book_ser = serializers.BookSerializer(query_set, data=request.data, partial=True)

        # 执行校验
        if book_ser.is_valid():
            # 校验后更新记录
            book_ser.save()     # 执行 self.update
            return Response(book_ser.validated_data)    # 校验成功数据
        else:
            return Response(book_ser.errors)            # 校验异常数据

    def delete(self, request, pk,  *arg, **kw):
        """
        删除记录
        """
        query_set = models.Books.objects.filter(id=pk).first()
        if query_set:
            query_set.delete()

        return Response()


# 第一次封装
class GenericAPIView(APIView):
    queryset = None
    serializer_class = None

    # 小技巧: 处理变量时 可定义入口函数
    def get_queryset(self):
        return self.queryset.all()

    def get_serializer(self, *arg, **kw):
        return self.serializer_class(*arg, **kw)








