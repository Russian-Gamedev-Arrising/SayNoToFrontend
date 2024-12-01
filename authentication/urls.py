from django.urls import path
from authentication.views import RegisterView, LoginView, LogoutView


urlpatterns = [
    path("v1/authentication/register/", RegisterView.as_view(), name='register'),
    path("v1/authentication/login/", LoginView.as_view(), name='login'),
    path("v1/authentication/logout/", LogoutView.as_view(), name='logout'),
]