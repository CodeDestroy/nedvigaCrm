from django.db import models


class ObjectStat(models.Model):
    obj = models.ForeignKey('BuyObject', on_delete=models.CASCADE, verbose_name='Объект')
    contacts = models.IntegerField(default=0, verbose_name='Совершившие контакты')
    favorites = models.IntegerField(default=0, verbose_name='Избранное')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    date = models.DateField(verbose_name='Дата')

    class Meta(object):
        app_label = 'main'
        db_table = 'object_stats'
        verbose_name = 'статистика по объекту'
        verbose_name_plural = 'статистика по объектам'
