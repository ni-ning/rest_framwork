# coding: utf-8

from rest_framework import serializers

from delta import models


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=32, default='')

    def create(self, validated_data):
        book = models.Books.objects.create(**validated_data)
        return book

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
