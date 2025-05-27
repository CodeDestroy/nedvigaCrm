from django.db import models

from . import CreatedUpdatedMixin


class Bank(CreatedUpdatedMixin):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    url = models.URLField(verbose_name='Ссылка на сайт', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta(object):
        app_label = 'main'
        db_table = 'banks'
        verbose_name = 'банк'
        verbose_name_plural = 'банки'
