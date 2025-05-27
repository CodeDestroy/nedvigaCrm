from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Wantresult(models.Model):
    vid = models.IntegerField(default=0, verbose_name='Уникальный идентификатор посетителя')
    num = models.SmallIntegerField(default=1, verbose_name='Какой из wantresult', help_text='1 - обычный; 2 - новый')
    site = models.CharField(max_length=50, verbose_name='Название домена')
    page = models.CharField(max_length=255, verbose_name='Страница, с которой произошло определение',
                            null=True, blank=True)
    ref = models.CharField(max_length=255, verbose_name='Страница, с которой посетитель перешел на страницу сайта',
                           null=True, blank=True)
    time = models.DateTimeField(verbose_name='Время определения в системе Timestamp')
    browser = models.CharField(max_length=50, verbose_name='Браузер', null=True, blank=True)
    device = models.CharField(max_length=50, verbose_name='Устройство', null=True, blank=True)
    platform = models.CharField(max_length=50, verbose_name='Платформа', null=True, blank=True)
    country = models.CharField(max_length=50, verbose_name='Страна', null=True, blank=True)
    region = models.CharField(max_length=50, verbose_name='Регион', null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name='Город', null=True, blank=True)
    ip = models.CharField(max_length=15, verbose_name='IP', null=True, blank=True)
    comment = models.CharField(max_length=255, verbose_name='Комментарий', null=True, blank=True)
    roistat_visit = models.IntegerField(default=0, verbose_name='Уникальный идентификатор посетителя в системе',
                                        null=True, blank=True)
    phones = models.JSONField(verbose_name='Номера телефонов', null=True, blank=True)
    mails = models.JSONField(verbose_name='Адреса электронной почты', null=True, blank=True)
    utm = models.JSONField(verbose_name='UTM-метки', null=True, blank=True)

    class Meta(object):
        app_label = 'main'
        db_table = 'wantresults'
        verbose_name = 'лид wantresult'
        verbose_name_plural = 'лиды wantresult'


@receiver(post_save, sender=Wantresult, dispatch_uid='create_update_wantresult')
def create_update_wantresult(instance, created, **kwargs):
    from django.core.exceptions import ObjectDoesNotExist
    from main.models import Lead, LeadSource, Source, Comment
    if instance.phones:
        for phone in instance.phones:
            try:
                lead = Lead.objects.get(phone=phone)
                lead.processed = 'redo'
                lead.save()
                Comment.objects.create(type='lead', item_id=lead.pk, text='Контакт продублировался из лидогенератора')
            except ObjectDoesNotExist:
                lead = Lead()
                lead.phone = phone
                lead.surname = 'Контакт от лидогенератора'
                lead.save()
                Comment.objects.create(type='lead', item_id=lead.pk, text='Контакт из лидогенератора создан автоматически')
            ls = LeadSource()
            ls.lead = lead
            if instance.utm:
                ls.utm = instance.utm
            else:
                ls.utm = {'site': instance.site, 'page': instance.page}
            if instance.num == 1:
                ls.source = Source.objects.get_or_create(name='Лидогенератор')[0]
            else:
                ls.source = Source.objects.get_or_create(name='Лидогенератор 2')[0]
            ls.save()
