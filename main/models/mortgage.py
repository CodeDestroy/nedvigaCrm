from django.db import models
from django.urls import reverse

from . import CreatedUpdatedMixin


class Mortgage(CreatedUpdatedMixin):
    deal = models.OneToOneField('Deal', on_delete=models.CASCADE, verbose_name='Сделка')
    max = models.FloatField(default=0, verbose_name='Максимально одобренная сумма')
    sum = models.FloatField(default=0, verbose_name='Выданная банком сумма')
    broker = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Ипотечный брокер',
                               null=True, blank=True)
    broker_status = models.CharField(max_length=15, choices=(
        ('consultation', 'Консультация'), ('collect_docs', 'Сбор документов'),
        ('review', 'Рассмотрение'), ('estate', 'Подбор недвижимости'), ('deal', 'Сделка'),
        ('bank_decline', 'Отказ банка'), ('client_decline', 'Отказ клиента'),
    ), verbose_name='Ипотечный статус', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('main:deal-page', kwargs={'deal_id': self.deal.pk})

    class Meta(object):
        app_label = 'main'
        ordering = ['-pk']
        db_table = 'mortgages'
        verbose_name = 'ипотека'
        verbose_name_plural = 'ипотеки'
