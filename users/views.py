from rest_framework.views import APIView
from rest_framework import exceptions, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class UserRegisterView(APIView):
    def post(self, request):
        if "username" not in request.data or "password" not in request.data or "email" not in request.data:
            raise exceptions.NotAcceptable(detail="Please enter username and password and email")
        username = request.data["username"]
        if User.objects.filter(username=username).count() != 0:
            raise exceptions.NotAcceptable(detail="Username already exists")
        password = request.data["password"]
        email = request.data["email"]
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return Response({
            "successful": True,
            "message": {
                "register": "user registered successfully"
            }
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        if "username" not in request.data or "password" not in request.data:
            raise exceptions.NotAcceptable(detail="Please enter username and password")
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if not user:
            raise exceptions.AuthenticationFailed(detail="Wrong user credentials")
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({
            "successful": True,
            "message": {
                "token": token.key,
            }
        }, status=status.HTTP_200_OK)
