from django.db import models


class LeadSource(models.Model):
    lead = models.ForeignKey('Lead', on_delete=models.CASCADE, verbose_name='Лид')
    source = models.ForeignKey('Source', on_delete=models.CASCADE, verbose_name='Источник')
    utm = models.JSONField(verbose_name='UTM-метки по которым пришли с источника', blank=True, null=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta(object):
        app_label = 'main'
        db_table = 'lead_sources'
        verbose_name = 'связь источника и лида'
        verbose_name_plural = 'связи источников и лидов'
