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
    '''
    if any image is deleted, user should not get deleted
    '''
    image = models.OneToOneField(Image, on_delete=models.DO_NOTHING, null=True, blank=True)


class Post(models.Model):
    '''
    if any user(author) is deleted, it should delete his posts as well
    '''
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    '''
    creating a string representation of the post model, which is the title of the post with upto 30 characters
    '''
    def __str__(self):
        data = (self.title[:30] + '..') if len(self.title) > 30 else self.title
        return data


class Comment(models.Model):
    """
    if any user(author) is deleted, it should delete his comments as well
    if any post is deleted, it should delete the comments as well
    """
    comment_text = models.CharField(max_length=300)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        data = (self.comment_text[:30] + '..') if len(self.comment_text) > 30 else self.comment_text
        return data

