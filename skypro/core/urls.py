from .views import (CreateAccountView, LoginView, ChangePasswordView, AccountView)
from django.urls import path


urlpatterns = [
    path('new_account', CreateAccountView.as_view(), name='new_account'),
    path('login', LoginView.as_view(), name='login'),
    path('account', AccountView.as_view(), name='account'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
]
