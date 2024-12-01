from django.urls import path
from .views import Register, Login, Logout

urlpatterns = [
    path('v1/authentication/register/', Register.as_view(), name='register'),
    path('v1/authentication/login/', Login.as_view(), name='login'),
    path('v1/authentication/logout/', Logout.as_view(), name='logout'),
]