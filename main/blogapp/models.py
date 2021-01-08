from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
from main import settings


class User(AbstractUser):
    image_url = models.CharField(max_length=300)


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        data = (self.title[:30] + '..') if len(self.title) > 30 else self.title
        return data



