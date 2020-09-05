from django.db import models


class Tokens(models.Model):
    access_token = models.SlugField(max_length=255)
    refresh_token = models.SlugField(max_length=255)
    ip_address = models.GenericIPAddressField(default="0.0.0.0")
