from django.db import models


class best_new_music(models.Model):
    album = models.CharField(max_length=128)
    artist = models.CharField(max_length=128)
    spotifyID = models.CharField(max_length=30)
    ip_address = models.GenericIPAddressField(default="0.0.0.0")
