from django.db import models

from . import CreatedUpdatedMixin


class Stage(CreatedUpdatedMixin):
    funnel = models.ForeignKey('Funnel', on_delete=models.CASCADE, verbose_name='Воронка продаж')
    parent = models.ForeignKey('Stage', on_delete=models.SET_NULL, verbose_name='Родитель', blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name='Название')
    statistic = models.BooleanField(default=False, verbose_name='Показывать стадию в статистике?')
    deal_close = models.BooleanField(default=False, verbose_name='Закрывать сделку при переносе в стадию?')
    good = models.BooleanField(default=False, verbose_name='Положительный статус')
    bad = models.BooleanField(default=False, verbose_name='Отрицательный статус')

    def __str__(self):
        return self.name

    def child(self):
        return Stage.objects.filter(parent=self).first()

    class Meta(object):
        app_label = 'main'
        db_table = 'stages'
        verbose_name = 'стадия продажи'
        verbose_name_plural = 'стадии продаж'
