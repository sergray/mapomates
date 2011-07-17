from django.db import models


class Profile(models.Model):
    cipher_text = models.CharField(max_length=36, unique=True, db_index=True)
    username = models.CharField(max_length=80, unique=True, db_index=True)
    portrait = models.URLField(verify_exists=False, blank=True, default='')
    lat = models.CharField(max_length=20, blank=True, default='')
    lon = models.CharField(max_length=20, blank=True, default='')
