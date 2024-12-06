from django.urls import path, include


urlpatterns = [
    path("v1/authentication/", include("djoser.urls")),
    path("v1/authentication/", include("djoser.urls.jwt")),
]
