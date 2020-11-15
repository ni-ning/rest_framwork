# coding: utf-8

from rest_framework import permissions


class MyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # 读取权限允许任何请求，即GET，HEAD或OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.city == '北京':
            return True
        else:
            return False
