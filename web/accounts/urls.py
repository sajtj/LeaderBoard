from django.urls import path
from .views import UserRegistrationView, login, LogoutAPIView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', login, name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
