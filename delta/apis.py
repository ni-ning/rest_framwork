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
        query_set = models.Books.objects.filter(id=pk)
        if query_set:
            query_set.delete()

        return Response({'msg': 'Success'})


# 第一次封装
class GenericAPIView(APIView):
    """
    把公共部分抽出来 queryset serializer_class
    """
    queryset = None
    serializer_class = None

    # 小技巧: 处理变量时 可定义入口函数
    def get_queryset(self):
        return self.queryset.all()

    def get_serializer(self, *arg, **kw):
        return self.serializer_class(*arg, **kw)


class ListModelMixin(object):
    # Mixin模式不能单独使用，其中包含其他类中方法，如get_queryset, get_serializer
    def list(self, request, *arg, **kw):
        """
        列表
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateModelMixin(object):
    def create(self, request, *arg, **kw):
        """
        创建
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors)


class RetrieveModelMixin(object):
    def retrieve(self, request, pk, *arg, **kw):
        """
        详情
        """
        obj = self.get_queryset().filter(pk=pk).first()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class UpdateModelMixin(object):
    def update(self, request, pk, *arg, **kw):
        """
        更新
        """
        obj = self.get_queryset().filter(pk=pk).first()
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors)


class DestroyModelMixin(object):
    def destroy(self, request, pk, *arg, **kw):
        """
        删除
        """
        query = self.get_queryset().filter(pk=pk)
        if query:
            query.delete()
        return Response({'msg': 'Success'})


class BookGenericView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = models.Books.objects.all()
    serializer_class = serializers.BookSerializer

    def get(self, request, *arg, **kw):
        return self.list(request, *arg, **kw)

    def post(self, request, *arg, **kw):
        return self.create(request, *arg, **kw)


class BookGenericDetail(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = models.Books.objects.all()
    serializer_class = serializers.BookSerializer

    def get(self, request, pk, *arg, **kw):
        return self.retrieve(request, pk, *arg, **kw)

    def put(self, request, pk, *arg, **kw):
        return self.update(request, pk, *arg, **kw)

    def delete(self, request, pk, *arg, **kw):
        return self.destroy(request, pk, *arg, **kw)


# 第二次封装
class ListCreateAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    pass


class RetrieveUpdateDestroyAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    pass


class BookListCreate(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = models.Books.objects.all()
    serializer_class = serializers.BookSerializer

    def get(self, request, *arg, **kw):
        return self.list(request, *arg, **kw)

    def post(self, request, *arg, **kw):
        return self.create(request, *arg, **kw)


class BookRetrieveUpdateDestroy(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = models.Books.objects.all()
    serializer_class = serializers.BookSerializer

    def get(self, request, pk, *arg, **kw):
        return self.retrieve(request, pk, *arg, **kw)

    def put(self, request, pk, *arg, **kw):
        return self.update(request, pk, *arg, **kw)

    def delete(self, request, pk, *arg, **kw):
        return self.destroy(request, pk, *arg, **kw)


# 第三次封装
from rest_framework.viewsets import ViewSetMixin


class ModelViewSet(ViewSetMixin, ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    pass


class BookModelViewSet(ModelViewSet):
    queryset = models.Books.objects.all()
    serializer_class = serializers.BookSerializer


from rest_framework import views
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets




