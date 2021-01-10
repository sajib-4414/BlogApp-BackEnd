from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageSerializer, PostSerializer
from rest_flex_fields.views import FlexFieldsModelViewSet
from main.blogapp.serializers import UserCreationSerializer, UserUpdateSerializer, UserOutputSerializer
from .models import Image, Post

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    permission_classes = (AllowAny,)


class UserRetrieveUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def validate_if_owner_logged_in(self,request, user):
        """
        Verifying the user is requesting profile information or updating, is Logged in with his profile
        """
        token_user = Token.objects.get(key=request.auth.key).user
        if token_user.username != user.username:
            raise ValidationError("You are not allowed to perform this action.")

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        self.validate_if_owner_logged_in(request,user)
        output_serializer = UserOutputSerializer(user)
        return Response(output_serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        self.validate_if_owner_logged_in(request,user)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            output_serializer = UserOutputSerializer(user)
            return Response(output_serializer.data)
            # return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSet(FlexFieldsModelViewSet):
    """
    this is a viewset, so it should support CRUD api
    """
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class PostsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    '''
    only for list and post
    '''
    def get(self, request, format=None):
        posts = Post.objects.all() #filter(user__username=request.user.username)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data.copy())
        # serializer.context["username"] = request.user.username #passing username, serializer will add the linked user later
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
