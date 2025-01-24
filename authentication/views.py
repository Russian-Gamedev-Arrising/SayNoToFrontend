from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from rest_framework.views import APIView
from allauth.socialaccount.models import SocialAccount, SocialToken
from allauth.socialaccount.helpers import complete_social_login
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from django.contrib.auth.models import User


class RegisterView(APIView):
    """Регистрация нового пользователя"""

    def post(self, request):
        login = request.data.get("login")
        email = request.data.get("email")
        password = request.data.get("password")

        if login is None or email is None or password is None:
            return Response(
                {"error": "Все поля обязательны"}, status=HTTP_400_BAD_REQUEST
            )

        if (
            User.objects.filter(username=login).exists()
            or User.objects.filter(email=email).exists()
        ):
            return Response(
                {"error": "Логин или email уже заняты"}, status=HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(username=login, email=email, password=password)
        # Генерация JWT токенов
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=HTTP_200_OK,
        )


class LoginView(APIView):
    """Авторизация пользователя"""

    def post(self, request):
        identifier = request.data.get("login_or_email")
        password = request.data.get("password")

        if identifier is None or password is None:
            return Response(
                {"error": "Необходимо указать логин/email и пароль"},
                status=HTTP_400_BAD_REQUEST,
            )
        # Ищем пользователя по логину или email
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            user = User.objects.filter(email=identifier).first()
        # Проверяем пароль
        if not user or not user.check_password(password):
            return Response(
                {"error": "Неверный логин/email или пароль"},
                status=HTTP_401_UNAUTHORIZED,
            )
        # Генерация JWT токенов
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
            },
            status=HTTP_200_OK,
        )


class LogoutView(APIView):
    """Выход из системы (аннулирование токена)"""

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Необходимо предоставить refresh токен."},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            # Отмечаем токен как недействительный
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Вы успешно вышли из системы"}, status=HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "Недействительный токен"},
                status=HTTP_400_BAD_REQUEST,
            )


class GitHubLogin(APIView):
    """
    Вход через GitHub с выдачей JWT-токена.
    """

    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")

        if not access_token:
            return Response(
                {"error": "Токен доступа не предоставлен."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        adapter = GitHubOAuth2Adapter()
        token = SocialToken(token=access_token)

        try:
            # Завершаем социальный вход через GitHub
            login = complete_social_login(request, adapter, token)
            user = login.user

            if not user.is_active:
                return Response(
                    {"error": "Пользователь не активен."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Проверяем или создаём SocialAccount
            social_account, _ = SocialAccount.objects.get_or_create(
                user=user,
                provider="github",
                defaults={"extra_data": token.token_secret},
            )

            # Генерируем JWT-токены
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                },
                status=HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
