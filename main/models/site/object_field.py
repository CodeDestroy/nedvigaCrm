from django.db import models


class ObjectField(models.Model):
    obj = models.ForeignKey('BuyObject', on_delete=models.CASCADE, verbose_name='Объект')
    name = models.CharField(max_length=75, verbose_name='Название поля')
    value = models.TextField(verbose_name='Значение')

    def get_tpl_name(self):
        return f'exclusive/form/{self.name}.html'

    class Meta(object):
        app_label = 'main'
        db_table = 'object_field'
        verbose_name = 'параметры объявления у объекта'
        verbose_name_plural = 'параметры объявлений у объектов'
