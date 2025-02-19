from django.conf import settings
from django.db import models

from . import CreatedUpdatedMixin


class Comment(CreatedUpdatedMixin):
    type = models.CharField(max_length=8, choices=settings.ITEM_TYPE_CHOICES, default='task',
                            verbose_name='Тип сущности')
    item_id = models.IntegerField(default=0, verbose_name='ID сущности')
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст комментария')
    deleted = models.BooleanField(default=False)

    def get_card_template(self):
        return 'comment/card.html'

    class Meta(object):
        app_label = 'main'
        ordering = ['-created_at']
        db_table = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
