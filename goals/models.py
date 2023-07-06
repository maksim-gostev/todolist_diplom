from django.db import models
from django.utils import timezone

from core.models import User


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)



class GoalCategory(BaseModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)


    def __str__(self):
        return self.title


class Goal(BaseModel):
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

    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT, related_name='goals')
    category = models.ForeignKey(GoalCategory, verbose_name='Категория', on_delete=models.PROTECT, related_name='goals')
    title = models.CharField(verbose_name='Название', max_length=250)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    due_date = models.DateField(verbose_name='Дата выполнения', null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус", choices=Status.choices, default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
    )

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    def __str__(self):
        return self.title


class GoalComment(BaseModel):
    text = models.TextField(verbose_name='Текст')
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    goal = models.ForeignKey(GoalCategory, verbose_name='Категория', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
