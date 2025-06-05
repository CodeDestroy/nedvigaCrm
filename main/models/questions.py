from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from . import CreatedUpdatedMixin


class Questions(CreatedUpdatedMixin):
    lead = models.OneToOneField('Lead', on_delete=models.CASCADE, verbose_name='Контакт')
    district = models.CharField(max_length=150, verbose_name='Район', null=True, blank=True)
    budget = models.CharField(max_length=150, verbose_name='Бюджет', null=True, blank=True)
    rooms = models.CharField(max_length=150, verbose_name='Количество комнат', null=True, blank=True)
    deadline = models.CharField(max_length=150, verbose_name='Срок сдачи', null=True, blank=True)
    purpose = models.CharField(max_length=7, verbose_name='Цель покупки', choices=settings.PURPOSE_BUY,
                               null=True, blank=True)
    decoration = models.CharField(max_length=15, verbose_name='Отделка', choices=settings.DECORATION_CHOICES,
                                  null=True, blank=True)
    developer = models.CharField(max_length=50, verbose_name='Застройщик', null=True, blank=True, choices=settings.DEVELOPERS_CHOICES)
    payment = models.CharField(max_length=9, verbose_name='Способы оплаты', choices=settings.PAYTYPE_CHOICES,
                               null=True, blank=True)
    bank = models.CharField(max_length=150, verbose_name='Банк', null=True, blank=True)
    maternity = models.BooleanField(default=False, verbose_name='Материнский капитал')
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    residence_place = models.CharField(max_length=150, verbose_name='Место проживания', blank=True, null=True)
    residence_birth = models.CharField(max_length=150, verbose_name='Место рождения', blank=True, null=True)
    marital_status = models.CharField(max_length=12, verbose_name='Семейное положение',
                                      choices=settings.MARITAL_CHOICES, blank=True, null=True)
    child_count = models.IntegerField(default=0, verbose_name='Количество детей')
    child_ages = models.CharField(max_length=150, verbose_name='Возраст детей', blank=True, null=True)

    class Meta(object):
        app_label = 'main'
        db_table = 'questions'
        verbose_name = 'вопросы контакта'
        verbose_name_plural = 'вопросы контактов'


def purpose(value):
    match value:
        case 'myself':
            return 'Для себя'
        case 'invest':
            return 'Инвестиции'
        case 'kids':
            return 'Детям'
        case _:
            return ''


def decoration(value):
    match value:
        case 'clean':
            return 'Чистовая'
        case 'black':
            return 'Черновая'
        case 'preclean':
            return 'Предчистовая'
        case _:
            return ''


def payment(value):
    match value:
        case 'cash':
            return 'Наличный расчет'
        case 'cashless':
            return 'Безналичный расчет'
        case 'mortgage':
            return 'Ипотека'
        case _:
            return ''


def marital(value):
    match value:
        case 'not_married':
            return 'Не замужем / не женат'
        case 'married':
            return 'Замужем / женат'
        case _:
            return ''
