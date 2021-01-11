from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from main.blogapp.models import Post, Image, Comment
# class CustomUserAdmin(UserAdmin):
#     pass
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserAdmin(UserAdmin):
    ...
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('image',)}),
    )

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Image)
# admin.site.register(User, CustomUserAdmin)
