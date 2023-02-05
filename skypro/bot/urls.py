from django.urls import path

from bot.views import TgVerificationView

urlpatterns = [
    path('verify', TgVerificationView.as_view(), name='verify-user'),
]
