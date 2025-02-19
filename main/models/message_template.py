from django.db import models


class MessageTemplate(models.Model):
    text = models.TextField(verbose_name='Шаблон сообщения')
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta(object):
        app_label = 'main'
        ordering = ['-created_at']
        db_table = 'message_templates'
        verbose_name = 'шаблон сообщения'
        verbose_name_plural = 'шаблоны сообщений'
