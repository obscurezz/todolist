from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(write_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_chat_id', 'tg_user_name', 'verification_code', 'user')
        read_only_fields = ('tg_chat_id', 'tg_user_name', 'user')

    def validate(self, attrs: dict):
        verification_code: str = attrs.get('verification_code')
        tg_user: QuerySet = TgUser.objects.filter(verification_code=verification_code).first()

        if not tg_user:
            raise ValidationError('Invalid verification code')

        attrs['tg_user'] = tg_user
        return attrs
