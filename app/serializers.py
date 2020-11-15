# coding: utf-8

from rest_framework import serializers

from app import models


class PublishSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=32)
    city = serializers.CharField(max_length=32)
    email = serializers.CharField(max_length=64)

    def create(self, validated_data):
        return models.Publish.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.city = validated_data.get('city', instance.city)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class ModelPublishSerializer(serializers.ModelSerializer):

    # Todo 诸如ReadOnlyField 和 source 用法
    # operator = serializers.ReadOnlyField(source='operator.username')

    class Meta:
        model = models.Publish
        fields = (
            'id',
            'name',
            'city',
            'email'
        )


class ModelBookSerializer(serializers.ModelSerializer):

    publish = serializers.StringRelatedField(source='publish.name')

    class Meta:
        model = models.Book
        fields = (
            'id',
            'title',
            'publish'
        )


class HyperlinkedBookSerializer(serializers.HyperlinkedModelSerializer):

    # ToDo 待测试
    class Meta:
        model = models.Book
        fields = (
            'id',
            'title',
            'publish'
        )
