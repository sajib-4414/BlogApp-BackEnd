"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main.blogapp import views
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views

router = routers.DefaultRouter()
router.register(r'images',views.ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('users/', views.UserCreateAPIView.as_view()),
    path('users/<int:pk>/', views.UserRetrieveUpdateAPIView.as_view()),
    path('posts/', views.PostsAPIView.as_view()),
    path('posts/<int:pk>/', views.PostDetailUpdateDeleteAPIView.as_view()),
    path('comments/', views.CommentsAPIView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailUpdateDeleteAPIView.as_view()),
    path('comments-by-post/<int:pk>/', views.CommentsOfaPostAPIView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += [
    path('auth-token/', authtoken_views.obtain_auth_token) # This one for getting Token
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
