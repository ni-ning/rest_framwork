from django.db import models


class Album(models.Model):
    album_name = models.CharField(max_length=128)
    artist = models.CharField(max_length=128)

    class Meta:
        db_table = 'nn_album'


class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=128)
    duration = models.IntegerField()

    class Meta:
        unique_together = ['album', 'order']
        ordering = ['order']
        db_table = 'nn_track'

    def __str__(self):
        return '%d: %s' % (self.order, self.title)



