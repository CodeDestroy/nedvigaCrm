from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from . import CreatedUpdatedMixin


class Lead(CreatedUpdatedMixin):
    surname = models.CharField(max_length=100, verbose_name='Фамилия', default='Новый клиент', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Имя', null=True, blank=True)
    patronymic = models.CharField(max_length=100, verbose_name='Отчество', null=True, blank=True)
    phone = models.CharField(unique=True, max_length=18, verbose_name='Номер телефона')
    email = models.CharField(max_length=100, verbose_name='E-mail', null=True, blank=True)
    complexes = models.JSONField(verbose_name='Интересующие комплексы', null=True, blank=True)
    client = models.ForeignKey('Lead', verbose_name='Клиент', on_delete=models.SET_NULL, null=True, blank=True)
    partner = models.ForeignKey('Partner', verbose_name='Агент', on_delete=models.SET_NULL, null=True, blank=True)
    first_manager = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Кто первым принял звонок',
                                      blank=True, null=True)
    responsible = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Ответственный',
                                    related_name='lead_responsible', blank=True, null=True)
    processed = models.CharField(verbose_name='Обработка', choices=settings.PROCESSED_CHOICES, default='not')
    warm = models.CharField(max_length=11, verbose_name='Теплота', choices=settings.LEAD_WARM_CHOICES,
                            blank=True, null=True)
    deferred = models.BooleanField(default=False, verbose_name='Отложенный спрос')
    spam = models.BooleanField(default=False, verbose_name='Спам?')
    is_deleted = models.BooleanField(default=False, verbose_name='Лид удален?')

    def __str__(self):
        return f'{self.surname if self.surname else ""} {self.name if self.name else ""} {self.patronymic if self.patronymic else ""}'.strip()

    def get_absolute_url(self):
        return reverse('main:lead-page', kwargs={'lead_id': self.pk})

    def client_deals(self):
        from main.models import Deal
        return Deal.objects.filter(lead__client=self)

    def comments(self):
        from main.models import Comment
        return Comment.objects.filter(type='lead', item_id=self.pk, deleted=False)

    def calls(self):
        from main.models import Call
        return Call.objects.filter(phone=self.phone)

    def warm_to_html(self):
        match self.warm:
            case 'hot':
                return '<span class="badge bg-red text-red-fg">Горячий</span>'
            case 'warm':
                return '<span class="badge bg-yellow text-yellow-fg">Теплый</span>'
            case 'cold':
                return '<span class="badge bg-azure text-azure-fg">Холодный</span>'
            case 'delayed':
                return '<span class="badge bg-lime text-lime-fg">Отложенный спрос</span>'
            case 'rent':
                return '<span class="badge bg-pink text-pink-fg">Аренда</span>'
            case 'not_client':
                return '<span class="badge bg-cyan-lt">Не клиент</span>'
            case 'not_call':
                return '<span class="badge badge-outline text-red">Не дозвонились</span>'
            case 'not_actual':
                return '<span class="badge bg-pink text-pink-fg">Не актуально</span>'
            case _:
                return '-'

    class Meta(object):
        app_label = 'main'
        ordering = ['-pk']
        db_table = 'leads'
        verbose_name = 'лид'
        verbose_name_plural = 'лиды'


def processed(value):
    match value:
        case 'not':
            return 'Не обработано'
        case 'complete':
            return 'Обработано'
        case 'pre':
            return 'Предварительно обработано'
        case 'redo':
            return 'Возвращено в обработку'
        case 'in_work':
            return 'Взят в работу'
        case _:
            return ''


def warm(value):
    match value:
        case 'hot':
            return 'Горячий'
        case 'warm':
            return 'Теплый'
        case 'cold':
            return 'Холодный'
        case 'delayed':
            return 'Отложенный спрос'
        case 'rent':
            return 'Аренда'
        case 'not_client':
            return 'Не клиент'
        case 'not_call':
            return 'Не дозвонились'
        case 'not_actual':
            return 'Не актуально'
        case _:
            return '-'


@receiver(post_save, sender=Lead, dispatch_uid='create_first_deal')
def create_update_log(instance, created, **kwargs):
    if created:
        from main.models import Deal
        if instance.first_manager:
            Deal.objects.create(lead=instance, name='Новая сделка', responsible=instance.first_manager)
        else:
            Deal.objects.create(lead=instance, name='Новая сделка')
    if instance.partner:
        from main.models import LeadSource, Source
        LeadSource.objects.get_or_create(lead=instance, source=Source.objects.get_or_create(name='Агентская сеть')[0])
    if instance.client:
        from main.models import LeadSource, Source
        LeadSource.objects.get_or_create(lead=instance, source=Source.objects.get_or_create(name='Клиентская сеть')[0])
