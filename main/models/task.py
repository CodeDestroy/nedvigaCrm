from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from main.models import Comment, CreatedUpdatedMixin


class Task(CreatedUpdatedMixin):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Исполнитель', related_name='task')
    priority = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)],
                                   verbose_name='Приоритет задачи')
    name = models.TextField(verbose_name='Название')
    text = models.TextField(verbose_name='Описание', blank=True, null=True)
    date_to = models.DateTimeField(verbose_name='Крайний срок', blank=True, null=True)
    is_done = models.BooleanField(default=False, verbose_name='Готово?')
    deal = models.ForeignKey('Deal', on_delete=models.SET_NULL, verbose_name='Сделка', blank=True, null=True)
    lead = models.ForeignKey('Lead', on_delete=models.SET_NULL, verbose_name='Лид', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_badge_color(self):
        match self.priority:
            case 2:
                return 'bg-blue'
            case 3:
                return 'bg-lime'
            case 4:
                return 'bg-yellow'
            case 5:
                return 'bg-red'

    def get_card_color(self):
        match self.priority:
            case 2:
                return 'bg-blue-lt'
            case 3:
                return 'bg-lime-lt'
            case 4:
                return 'bg-yellow-lt'
            case 5:
                return 'bg-red-lt'

    def get_absolute_url(self):
        return reverse('main:task-page', kwargs={'task_id': self.pk})

    def comments(self):
        return Comment.objects.filter(type='task', item_id=self.pk, deleted=False)

    class Meta(object):
        ordering = ['date_to']
        app_label = 'main'
        db_table = 'tasks'
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'
