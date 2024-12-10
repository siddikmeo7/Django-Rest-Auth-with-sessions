from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework import serializers
from api.serializers import *
from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        User = get_user_model()
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials')
        token, created = Token.objects.get_or_create(user=user)
        update_last_login(None, user)
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)



