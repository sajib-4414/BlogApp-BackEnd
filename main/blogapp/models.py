from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
from versatileimagefield.fields import VersatileImageField, PPOIField
from main import settings


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    image_url = models.CharField(max_length=300)
    image = models.OneToOneField(Image, on_delete=models.DO_NOTHING, null=True, blank=True)


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        data = (self.title[:30] + '..') if len(self.title) > 30 else self.title
        return data



