from django.db import models


class AllHighlyRatedAlbums(models.Model):
    album = models.CharField(max_length=128)
    artist = models.CharField(max_length=128)
    date = models.DateField()


class AllBestNewMusic(models.Model):
    album = models.CharField(max_length=128)
    artist = models.CharField(max_length=128)
    date = models.DateField()
