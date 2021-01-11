from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from main.blogapp.models import Post
from main.blogapp.serializers import PostOutputSerializer, PostInputSerializer, PostUpdateSerializer
User = get_user_model()


def get_logged_in_username(request):
    token_user = Token.objects.get(key=request.auth.key).user
    return token_user.username


def validate_if_post_or_comment_owner_logged_in(request, post):
    """
    Verifying the user is requesting profile information or updating, is Logged in with his profile
    """
    token_user = Token.objects.get(key=request.auth.key).user
    if token_user.username != post.author.username:
        raise ValidationError("You are not allowed to perform this action.")


def get_post_object(pk):
    try:
        return Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404


class PostsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    '''
    only for list and creation
    '''
    def get(self, request, format=None):
        logged_in_username = get_logged_in_username(request)
        posts = Post.objects.all().filter(author__username=logged_in_username)
        serializer = PostOutputSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostInputSerializer(data=request.data.copy())
        logged_in_username = get_logged_in_username(request)
        serializer.context["username"] = logged_in_username
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailUpdateDeleteAPIView(APIView):
    """
    Retrieve, update or delete a post instance.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        """
        anyone should be able to view any post
        """
        post = get_post_object(pk)
        serializer = PostOutputSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        only author should be able to update his post
        """
        post = get_post_object(pk)
        validate_if_post_or_comment_owner_logged_in(request, post)
        serializer = PostUpdateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        only author should be able to delete his post
        """
        post = get_post_object(pk)
        validate_if_post_or_comment_owner_logged_in(request, post)
        post.delete()
        return Response({"delete": "delete success"},status=status.HTTP_204_NO_CONTENT)
