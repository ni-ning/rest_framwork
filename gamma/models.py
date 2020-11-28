from django.db import models


class UserInfo(models.Model):

    user_type_choices = (
        (1, 'Normal'),
        (2, 'VIP'),
        (3, 'SVIP')
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)

    class Meta:
        db_table = 'nn_user_info'

    def __str__(self):
        return '<UserInfo object %s>' % self.username


class UserToken(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=64)

    # 次数或有效期验证

    class Meta:
        db_table = 'nn_user_token'

    def __str__(self):
        return '<UserToken object>'
