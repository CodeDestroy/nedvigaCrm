from django.db import models

from . import CreatedUpdatedMixin


class Partner(CreatedUpdatedMixin):
    surname = models.CharField(max_length=100, verbose_name='Фамилия', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Имя', null=True, blank=True)
    patronymic = models.CharField(max_length=100, verbose_name='Отчество', null=True, blank=True)
    phone = models.CharField(unique=True, max_length=18, verbose_name='Номер телефона')
    email = models.CharField(max_length=100, verbose_name='Адрес электронной почты', null=True, blank=True)
    company = models.CharField(max_length=120, verbose_name='Компания', null=True, blank=True)
    deleted = models.BooleanField(default=False, verbose_name='Удален?')

    def __str__(self):
        return f'{self.surname if self.surname else ""} {self.name if self.name else ""} {self.patronymic if self.patronymic else ""}'.strip()

    def deals(self):
        from main.models import Deal
        return Deal.objects.filter(lead__partner=self)

    class Meta(object):
        app_label = 'main'
        ordering = ['-created_at']
        db_table = 'partners'
        verbose_name = 'партнер'
        verbose_name_plural = 'партнеры'
