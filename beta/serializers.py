# coding: utf-8

import time

from rest_framework import serializers
from beta import models


class Role(object):
    ADMIN = 1
    TEACHER = 2
    STUDENT = 3
    GUEST = 4

    CHOICES = (
        (1, "Admin"),
        (2, "Teacher"),
        (3, "Student"),
        (4, "Guest")
    )


class TestingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    has_bool = serializers.BooleanField(allow_null=True)    # 验证时取值比较丰富 [True, 'TRUE', 'True', 'true'] -> True
    name = serializers.CharField(allow_blank=True, trim_whitespace=True, max_length=128, min_length=None)  # allow_blank
    age = serializers.IntegerField(min_value=0, max_value=128)
    salary = serializers.FloatField(min_value=0, max_value=None)
    role = serializers.ChoiceField(choices=Role.CHOICES, initial=Role.GUEST)
    create_time = serializers.DateTimeField(required=True)
    create_days = serializers.SerializerMethodField()   # source='*' read_only=True
    create_days_v1 = serializers.IntegerField(source='get_create_days')

    scores = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=100),
        allow_empty=True
    )
    document = serializers.DictField(child=serializers.CharField(), allow_empty=True)

    def get_create_days(self):
        return 100


class AlbumSerializer1(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)  # tracks 为 related_name='tracks', 否则抛无属性异常

    class Meta:
        model = models.Album
        fields = ['album_name', 'artist', 'tracks']


class AlbumSerializer2(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Album
        fields = ['album_name', 'artist', 'tracks']


# 取关联字段的相关属性，如SlugRelatedField -> slug_field
# 类似 source 含义
class AlbumSerializer3(serializers.ModelSerializer):
    tracks = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = models.Album
        fields = ['album_name', 'artist', 'tracks']


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Track
        fields = ['order', 'title', 'duration']


class AlbumSerializer4(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)     # 处理流程：Album -> tracks -> Track -> TrackSerializer

    class Meta:
        model = models.Album
        fields = ['album_name', 'artist', 'tracks']


class AlbumSerializer5(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)         # read_only=True, is_valid可以通过，但是save()时会抛异常

    class Meta:
        model = models.Album
        fields = ['album_name', 'artist', 'tracks']

    # create 只是一个入口，里面的逻辑自定义 自己来 返回 instance 就行
    def create(self, validated_data):
        # 自己处理输入参数
        tracks_data = validated_data.pop('tracks')

        # **validated_data
        album = models.Album.objects.create(**validated_data)

        for track_data in tracks_data:
            # album=album
            models.Track.objects.create(album=album, **track_data)
        return album


class TrackListingField(serializers.RelatedField):

    def to_representation(self, value):
        duration = time.strftime('%M:%S', time.gmtime(int(value.duration)))
        return 'Track %d: %s (%s)' % (value.order, value.title, duration)


# 自定义关联子模型
class AlbumSerializer6(serializers.ModelSerializer):
    tracks = TrackListingField(many=True, read_only=True)

    class Meta:
        model = models.Album
        fields = ['album_name', 'artist', 'tracks']