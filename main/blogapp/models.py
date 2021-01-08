from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        data = (self.title[:30] + '..') if len(self.title) > 30 else self.title
        return data

