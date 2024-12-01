from django.urls import path
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('api/v1/authentication/register/', RegisterView.as_view(), name='register'),
    path('api/v1/authentication/login/', LoginView.as_view(), name='login'),
    path('api/v1/authentication/logout/', LogoutView.as_view(), name='logout'),
]
