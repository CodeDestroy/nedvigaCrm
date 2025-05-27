from django.db import models

from . import CreatedUpdatedMixin


class Passport(CreatedUpdatedMixin):
    lead = models.OneToOneField('Lead', on_delete=models.CASCADE, verbose_name='Лид')
    seria = models.CharField(max_length=10, verbose_name='Серия', null=True, blank=True)
    number = models.CharField(max_length=10, verbose_name='Номер', null=True, blank=True)
    date = models.DateField(verbose_name='Дата выпуска', null=True, blank=True)
    whom = models.CharField(max_length=150, verbose_name='Кем выдан', null=True, blank=True)
    address_registration = models.CharField(max_length=150, verbose_name='Адрес регистрации', null=True, blank=True)
    address_actual = models.CharField(max_length=150, verbose_name='Адрес проживания', null=True, blank=True)

    class Meta(object):
        app_label = 'main'
        db_table = 'passports'
        verbose_name = 'паспорт'
        verbose_name_plural = 'паспорта'
