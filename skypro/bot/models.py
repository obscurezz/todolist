from django.db import models

from core.models import User


class TgUser(models.Model):
    objects = models.Manager()

    class Meta:
        verbose_name = 'TgUser'
        verbose_name_plural = 'TgUsers'

    tg_chat_id = models.PositiveIntegerField(verbose_name='tg chat_id', unique=True)
    tg_user_name = models.CharField(verbose_name='tg username', max_length=256, default=None)
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.PROTECT, null=True, db_column='user')
    verification_code = models.CharField(max_length=32, null=True)
