from django.db import models
from django.urls import reverse


class Source(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    color = models.CharField(max_length=12, verbose_name='Цвет стикера', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона при котором срабатывает источник',
                             null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:source-list')

    class Meta(object):
        app_label = 'main'
        db_table = 'sources'
        verbose_name = 'источник лида'
        verbose_name_plural = 'источники лидов'
