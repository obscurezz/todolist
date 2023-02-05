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


class Board(BaseModelMixin):
    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    title = models.CharField(verbose_name='Название', max_length=255)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)

    def __str__(self):
        return self.title


class BoardParticipant(BaseModelMixin):
    class Meta:
        unique_together = ('board', 'user')
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    class Role(models.IntegerChoices):
        owner = 1, 'Owner'
        writer = 2, 'Writer'
        reader = 3, 'Reader'

    board = models.ForeignKey(Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='participants')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT, related_name='participants')
    role = models.PositiveSmallIntegerField(verbose_name='Роль', choices=Role.choices, default=Role.owner)

    def __str__(self):
        return self.user.username


class GoalCategory(BaseModelMixin):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255, unique=True)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories",
                              db_column="board")

    def __str__(self):
        return self.title


class Goal(BaseModelMixin):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

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

    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT, db_column="category")
    title = models.CharField(verbose_name="Название", max_length=255, unique=True)
    description = models.CharField(verbose_name="Описание", max_length=1000, null=True, blank=True)
    due_date = models.DateField(verbose_name="Дата выполнения", null=True, blank=True)
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=Priority.choices,
                                                default=Priority.medium)
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор", db_column="user")

    def __str__(self):
        return self.title


class GoalComment(BaseModelMixin):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    text = models.CharField(verbose_name="Текст", max_length=4000)
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE, db_column="goal")
