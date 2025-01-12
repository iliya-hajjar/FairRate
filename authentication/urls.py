# authentication/urls.py
from django.urls import path
from .views import UserRegistrationView, CustomLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomLoginView.as_view(), name='user-login'),
]
