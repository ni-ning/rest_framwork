from django.db import models


class Publish(models.Model):
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    email = models.CharField(max_length=64)

    # operator = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING, default=-1)

    def __str__(self):
        return '<Publish %s>' % self.name

    class Meta:
        verbose_name = '出版社'
        verbose_name_plural = verbose_name
        db_table = 'nn_publish'


class Book(models.Model):
    title = models.CharField(max_length=64)
    publish = models.ForeignKey(Publish, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '<Book %s>' % self.title

    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = verbose_name
        db_table = 'nn_book'
