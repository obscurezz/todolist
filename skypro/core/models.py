from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, BooleanField


class User(AbstractUser):
    USERNAME_FIELD = 'username'

    first_name = CharField(max_length=50, null=True, blank=True)
    last_name = CharField(max_length=50, null=True, blank=True)
    username = CharField(max_length=50, unique=True, default='blank')
    email = EmailField(unique=True)
    is_active = BooleanField(null=False, default=True)
