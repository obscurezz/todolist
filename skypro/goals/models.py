from django.db import models
from django.utils import timezone

from core.models import User


class GoalCategory(models.Model):
    objects = models.Manager()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=timezone.now())
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=timezone.now())
