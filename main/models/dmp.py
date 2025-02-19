from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Dmp(models.Model):
    visit_id = models.IntegerField()
    phone = models.CharField(max_length=25, verbose_name='Телефон')
    timestamp = models.DateTimeField(verbose_name='Время визита')
    website = models.CharField(max_length=255, verbose_name='Домен сайта', null=True, blank=True)
    page = models.CharField(max_length=255, verbose_name='Страница сайта', null=True, blank=True)
    page_with_parameters = models.CharField(max_length=255, verbose_name='Страница сайта', help_text='С параметрами',
                                            null=True, blank=True)
    yid = models.CharField(max_length=125, verbose_name='Идентификатор', null=True, blank=True)
    email = models.JSONField(verbose_name='Почта', null=True, blank=True)
    vk = models.CharField(max_length=125, verbose_name='VK', null=True, blank=True)
    fb = models.CharField(max_length=125, verbose_name='Facebook', null=True, blank=True)
    insta = models.CharField(max_length=125, verbose_name='Instagram', null=True, blank=True)
    ok = models.CharField(max_length=125, verbose_name='OK', null=True, blank=True)
    utm_source = models.CharField(max_length=125)
    utm_medium = models.CharField(max_length=125)
    utm_campaign = models.CharField(max_length=125)
    utm_term = models.CharField(max_length=125)
    utm_content = models.CharField(max_length=125)
    referer = models.CharField(max_length=125)
    ip = models.CharField(max_length=16)
    stock_key = models.CharField(max_length=255)

    class Meta(object):
        app_label = 'main'
        db_table = 'dmp_one'
        verbose_name = 'dmp.one'
        verbose_name_plural = 'dmp.one`s'


@receiver(post_save, sender=Dmp, dispatch_uid='create_update_dmp')
def create_update_dmp(instance, created, **kwargs):
    from django.core.exceptions import ObjectDoesNotExist
    from main.models import Lead, LeadSource, Source, Comment
    try:
        lead = Lead.objects.get(phone=instance.phone)
        lead.processed = 'redo'
        lead.save()
        Comment.objects.create(type='lead', item_id=lead.pk, text='Контакт продублировался из лидогенератора')
    except ObjectDoesNotExist:
        lead = Lead()
        lead.phone = instance.phone
        lead.surname = 'Контакт из лидогенератора'
        lead.save()
        Comment.objects.create(type='lead', item_id=lead.pk, text='Контакт из лидогенератора создан автоматически')
    LeadSource.objects.create(lead=lead, utm={
        'source': instance.utm_source, 'medium': instance.utm_medium, 'campaign': instance.utm_campaign,
        'term': instance.utm_term, 'content': instance.utm_content}, source=Source.objects.get_or_create(
        name='Лидогенератор 3')[0])
