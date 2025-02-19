from django.db import models
from django.urls import reverse

from main.models import Comment, CreatedUpdatedMixin


class Showing(CreatedUpdatedMixin):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Исполнитель', related_name='showing')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    date_to = models.DateTimeField(verbose_name='Крайний срок', blank=True, null=True)
    is_done = models.BooleanField(default=False, verbose_name='Готово?')
    project = models.JSONField(verbose_name='Проект ЖК', null=True, blank=True)
    deal = models.ForeignKey('Deal', on_delete=models.SET_NULL, verbose_name='Сделка', blank=True, null=True)
    lead = models.ForeignKey('Lead', on_delete=models.SET_NULL, verbose_name='Лид', blank=True, null=True)

    def __str__(self):
        return f'Показ объекта "{self.project.name}"' if self.project else f'Показ #{self.id}'

    def get_absolute_url(self):
        return reverse('main:showing-page', kwargs={'showing_id': self.pk})

    def comments(self):
        return Comment.objects.filter(type='showing', item_id=self.pk, deleted=False)

    class Meta(object):
        ordering = ['date_to']
        app_label = 'main'
        db_table = 'showings'
        verbose_name = 'показ объекта'
        verbose_name_plural = 'показы объектов'
