from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny
from main.blogapp.serializers import UserInputOutputSerializer
from .models import Image

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInputOutputSerializer
    permission_classes = (AllowAny,)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserInputOutputSerializer
    permission_classes = (AllowAny,)

class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInputOutputSerializer
    permission_classes = (AllowAny,)

from .serializers import ImageSerializer
from rest_flex_fields.views import FlexFieldsModelViewSet

class ImageViewSet(FlexFieldsModelViewSet):

    serializer_class = ImageSerializer
    queryset = Image.objects.all()
