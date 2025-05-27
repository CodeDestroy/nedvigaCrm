from django.db import models


class Phone(models.Model):
    sip = models.CharField(max_length=10, verbose_name='SIP-номер', unique=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.sip

    class Meta(object):
        app_label = 'main'
        db_table = 'phones'
        verbose_name = 'SIP-номер'
        verbose_name_plural = 'SIP-номера'
