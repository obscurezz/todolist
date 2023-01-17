from .views import (CreateAccountView, LoginView, ChangePasswordView, ProfileView)
from django.urls import path


urlpatterns = [
    path('signup', CreateAccountView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_password', ChangePasswordView.as_view(), name='update_password'),
]
