from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from main.blogapp.serializers import UserCreationSerializer, UserUpdateSerializer, UserOutputSerializer
from .models import Image

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    permission_classes = (AllowAny,)


class UserRetrieveUpdateAPIView(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        todo = self.get_object(pk)
        output_serializer = UserOutputSerializer(todo)
        return Response(output_serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)

        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            output_serializer = UserOutputSerializer(user)
            return Response(output_serializer.data)
            # return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserUpdateAPIView(generics.UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserUpdateSerializer
#     permission_classes = (AllowAny,)

from .serializers import ImageSerializer
from rest_flex_fields.views import FlexFieldsModelViewSet

class ImageViewSet(FlexFieldsModelViewSet):

    serializer_class = ImageSerializer
    queryset = Image.objects.all()
