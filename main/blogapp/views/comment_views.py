from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from main.blogapp.models import Comment
from main.blogapp.serializers import CommentOutputSerializer, CommentInputSerializer
from main.blogapp.views import get_logged_in_username
from rest_framework.response import Response


def get_comment_object(pk):
    try:
        return Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        raise Http404


class CommentsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    '''
    only for list and creation
    '''
    def get(self, request, format=None):
        logged_in_username = get_logged_in_username(request)
        comments = Comment.objects.all().filter(author__username=logged_in_username)
        serializer = CommentOutputSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentInputSerializer(data=request.data.copy())
        logged_in_username = get_logged_in_username(request)
        serializer.context["username"] = logged_in_username
        if serializer.is_valid():
            created_comment = serializer.save()
            output_serializer = CommentOutputSerializer(created_comment)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CommentDetailUpdateDeleteAPIView(APIView):
#     """
#     Retrieve, update or delete a post instance.
#     """
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, pk, format=None):
#         """
#         anyone should be able to view any post
#         """
#         post = get_post_object(pk)
#         serializer = PostOutputSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         """
#         only author should be able to update his post
#         """
#         post = get_post_object(pk)
#         validate_if_post_owner_logged_in(request,post)
#         serializer = PostUpdateSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         """
#         only author should be able to delete his post
#         """
#         post = get_post_object(pk)
#         validate_if_post_owner_logged_in(request,post)
#         post.delete()
#         return Response({"delete": "delete success"},status=status.HTTP_204_NO_CONTENT)
