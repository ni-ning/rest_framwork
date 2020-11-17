# coding: utf-8

from rest_framework import serializers


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

    has_bool = serializers.BooleanField(allow_null=True)    # 验证时取值比较丰富 [True, 'TRUE', 'True', 'true'] -> True
    name = serializers.CharField(allow_blank=True, trim_whitespace=True, max_length=128, min_length=None)  # allow_blank
    age = serializers.IntegerField(min_value=0, max_value=128)
    salary = serializers.FloatField(min_value=0, max_value=None)
    role = serializers.ChoiceField(choices=Role.CHOICES, initial=Role.GUEST)
    create_time = serializers.DateTimeField(required=True)
    create_days = serializers.SerializerMethodField()   # source='*' read_only=True

    scores = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=100),
        allow_empty=True
    )
    document = serializers.DictField(child=serializers.CharField(), allow_empty=True)

    def get_create_days(self):
        return 100

