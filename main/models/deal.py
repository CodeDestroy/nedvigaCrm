from django.conf import settings
from django.db import models
from django.urls import reverse

from . import CreatedUpdatedMixin


class Deal(CreatedUpdatedMixin):
    lead = models.ForeignKey('Lead', on_delete=models.SET_NULL, verbose_name='Контакт', null=True, blank=True)
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, verbose_name='Стадия продажи',
                              null=True, blank=True)
    buy_object = models.ForeignKey('BuyObject', on_delete=models.SET_NULL, verbose_name='Объект', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='Название сделки')
    paytype = models.CharField(max_length=10, choices=settings.PAYTYPE_CHOICES, verbose_name='Тип платежа',
                               blank=True, null=True)
    legal_status = models.CharField(max_length=15, choices=(
        ('consultation', 'Консультация'), ('collect_docs', 'Сбор документов'),
        ('deposit', 'Задаток'), ('closing_deal', 'Закрытие сделки'),
    ), verbose_name='Юридический статус', null=True, blank=True)
    price = models.FloatField(default=0, verbose_name='Цена объекта')
    developer = models.CharField(max_length=120, verbose_name='Застройщик', null=True, blank=True)
    office = models.BooleanField(default=False, verbose_name='Подана в офисе')
    solution = models.BooleanField(default=False, verbose_name='Готовое решение')
    responsible = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Ответственный',
                                    related_name='deal_responsible', blank=True, null=True)
    bank = models.ForeignKey('Bank', on_delete=models.SET_NULL, verbose_name='Банк', blank=True, null=True)
    frm = models.CharField(max_length=10, verbose_name='Через', db_column='from', choices=settings.FROM_CHOICES,
                           blank=True, null=True)
    sell_date = models.DateField(null=True, blank=True, verbose_name='Дата сделки')
    notes = models.TextField(verbose_name='Особые отметки', blank=True, null=True)
    reserved = models.DateField(null=True, blank=True, verbose_name='Бронь')
    partner_paid = models.BooleanField(default=False, verbose_name='Партнерские выплачены?')
    spam = models.BooleanField(default=False, verbose_name='Спам?')

    def __str__(self):
        return self.name

    def partner_money(self):
        if self.price < 4000000:
            return 2000
        elif 4000000 <= self.price < 7000000:
            return 3000
        return 5000

    def get_absolute_url(self):
        return reverse('main:deal-page', kwargs={'deal_id': self.pk})

    def comments(self):
        from main.models import Comment
        return Comment.objects.filter(type='deal', item_id=self.pk, deleted=False)

    def paytype_text(self):
        match self.paytype:
            case 'cash':
                return 'Наличный расчет'
            case 'cashless':
                return 'Безналичный расчет'
            case 'mortgage':
                return 'Ипотека'
            case _:
                return ''

    class Meta(object):
        app_label = 'main'
        ordering = ['-pk']
        db_table = 'deals'
        verbose_name = 'сделка'
        verbose_name_plural = 'сделки'


def paytype(value):
    match value:
        case 'cash':
            return 'Наличный расчет'
        case 'cashless':
            return 'Безналичный расчет'
        case 'mortgage':
            return 'Ипотека'
        case _:
            return ''


def frm(value):
    match value:
        case 'nmarket':
            return 'Нмаркет'
        case 'perv':
            return 'Первичка'
        case 'contract':
            return 'Прямой договор'
        case _:
            return ''
