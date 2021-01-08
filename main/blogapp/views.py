from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import generics
from rest_framework.permissions import AllowAny
from main.blogapp.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
