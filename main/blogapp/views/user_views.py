from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from main.blogapp.serializers import UserCreationSerializer, UserUpdateSerializer, UserOutputSerializer
User = get_user_model()


def get_user_object(pk):
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404


def validate_if_owner_logged_in(request, user):
    """
    Verifying the user is requesting profile information or updating, is Logged in with his profile
    """
    token_user = Token.objects.get(key=request.auth.key).user
    if token_user.username != user.username:
        raise ValidationError("You are not allowed to perform this action.")


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    permission_classes = (AllowAny,)


class UserRetrieveUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        user = get_user_object(pk)
        validate_if_owner_logged_in(request,user)
        output_serializer = UserOutputSerializer(user)
        return Response(output_serializer.data)

    def put(self, request, pk, format=None):
        user = get_user_object(pk)
        validate_if_owner_logged_in(request,user)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            output_serializer = UserOutputSerializer(user)
            return Response(output_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
