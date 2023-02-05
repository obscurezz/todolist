from django.contrib import admin

from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('tg_chat_id', 'tg_user_name', 'user')
    read_only_fields = ('tg_chat_id', 'verification_code')
