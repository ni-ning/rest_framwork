# coding: utf-8

from rest_framework import serializers

from gamma import models


class RoleSerializer(serializers.Serializer):

    # 和数据库中字段一致
    id = serializers.IntegerField()
    title = serializers.CharField()


class UserInfoSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()
    # user_type = serializers.IntegerField()
    xxxx = serializers.CharField(source='user_type')                    # source 对应数据的字段来源 row.user_type
    user_type = serializers.CharField(source='get_user_type_display')   # row.get_user_type_display()

    gp_obj_str = serializers.CharField(source='group')
    gp_id = serializers.CharField(source='group.id')
    gp_title = serializers.CharField(source='group.title')

    # role_list = serializers.CharField(source='roles.all')     # ManyToMany做不多特别细的粒度
    role_list = serializers.SerializerMethodField()             # 自定义显示

    def get_role_list(self, row):
        return [RoleSerializer(role).data for role in row.roles.all()]


class UserInfoModelSerializer(serializers.ModelSerializer):

    # 与Serializer混合着用
    xxxx = serializers.CharField(source='user_type')
    user_type = serializers.CharField(source='get_user_type_display')

    class Meta:
        model = models.UserInfo
        # fields = '__all__'
        fields = ['id', 'username', 'password', 'xxxx', 'user_type', 'group']
        depth = 1
