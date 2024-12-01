from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
# Create your views here.



class Register(APIView):
    '''Регистрация нового пользователя'''
    def post(self, request):
        login = request.data.get("login")
        email = request.data.get("email")
        password = request.data.get("password")

        if login == None or email == None or password == None:
            return Response({"error": "Все поля обязательны"}, status=HTTP_400_BAD_REQUEST)
        
        '''добавить проверку на то что уже есть почта или логин'''
        
        user = User.objects.create_user(username=login, email=email, password=password)
        token = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)


class Login(APIView):
    '''Авторизация пользователя'''

    def get(self, request):
        identifier = request.query_params.get("login/email")
        password = request.query_params.get("password")

        if not all([identifier, password]):
            return Response({"error": "Необходимо указать логин/email и пароль"}, status=HTTP_400_BAD_REQUEST)

        user = authenticate(username=identifier, password=password) or authenticate(email=identifier, password=password)
        if user is None:
            return Response({"error": "Неверный логин/email или пароль"}, status=HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)


class Logout(APIView):
    """ Выход из системы (аннулирование токена)"""

    def get(self, request):
        token_key = request.query_params.get("token")
        if not token_key:
            return Response({"error": "Токен обязателен"}, status=HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(key=token_key)
            token.delete()
            return Response({"message": "Вы успешно вышли из системы"}, status=HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Токен недействителен"}, status=HTTP_401_UNAUTHORIZED)