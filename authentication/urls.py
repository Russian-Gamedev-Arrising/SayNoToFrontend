from django.urls import path, include
from django.urls import path
from .views import GitHubLogin
from .views import GoogleLoginView

urlpatterns = [
    # Djoser для управления пользователями
    path("v1/authentication/", include("djoser.urls")),
    path("v1/authentication/", include("djoser.urls.jwt")),
    # Социальный логин через GitHub
    path("v1/authentication/github/", GitHubLogin.as_view(), name="github-login"),
    path("v1/authentication/google/", GoogleLoginView.as_view(), name="google-login"),
]
