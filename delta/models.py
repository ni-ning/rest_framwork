from django.db import models


class Books(models.Model):
    name = models.CharField(max_length=32, help_text='书名')

    class Meta:
        db_table = 'nn_books'

    def __str__(self):
        return '<Book %s>' % self.name


