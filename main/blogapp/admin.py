from django.contrib import admin

# Register your models here.
from main.blogapp.models import Post

admin.site.register(Post)
