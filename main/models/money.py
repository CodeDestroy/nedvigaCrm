from django.db import models

from . import CreatedUpdatedMixin


class Money(CreatedUpdatedMixin):
    deal = models.OneToOneField('Deal', on_delete=models.CASCADE, verbose_name='Сделка')
    agent = models.FloatField(verbose_name='Комиссия агентства', default=0)
    paid = models.FloatField(verbose_name='Выплаченные средства', default=0)
    manager = models.FloatField(verbose_name='Комиссия менеджера', default=0)
    get = models.BooleanField(default=False, verbose_name='Выплата получена')
    get_date = models.DateField(null=True, blank=True, verbose_name='Когда получена выплата')
    status = models.CharField(max_length=10, choices=(
        ('wait', 'Ожидаем'), ('receive', 'Получено'), ('think', 'Думают')
    ), verbose_name='Статус комиссии', default='think')
    bill_date = models.DateField(null=True, blank=True, verbose_name='Когда передан счет')
    planned_date = models.DateField(null=True, blank=True, verbose_name='Планируемая дата получения денег')

    def com_manager(self):
        return 0

    def com_diff(self):
        if self.paid > 0:
            return self.agent - self.paid
        return 0

    def get_card_template(self):
        return 'tabs/cards/money.html'

    class Meta(object):
        app_label = 'main'
        ordering = ['-pk']
        db_table = 'moneys'
        verbose_name = 'деньги по сделке'
        verbose_name_plural = 'деньги по сделкам'
