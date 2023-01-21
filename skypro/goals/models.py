from django.db import models
from django.utils import timezone

from core.models import User


class BaseModelMixin(models.Model):
    class Meta:
        abstract = True

    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=timezone.now())
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=timezone.now())


class GoalCategory(BaseModelMixin):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Status(models.IntegerChoices):
    to_do = 1, "К выполнению"
    in_progress = 2, "В процессе"
    done = 3, "Выполнено"
    archived = 4, "Архив"


class Priority(models.IntegerChoices):
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"


class Goal(BaseModelMixin):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.CharField(verbose_name="Описание", max_length=2000)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=Priority.choices,
                                                default=Priority.medium)
    deadline = models.DateField(verbose_name="Дата дедлайна")
