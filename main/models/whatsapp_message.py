from django.db import models

direction_choices = (
    ('in', 'Входящее'),
    ('out', 'Исходящее')
)

status_choices = (
    ('deleted', 'Удалено'),
    ('delivered', 'Отправлено'),
    ('failed', 'Неудачно'),
    ('read', 'Прочитано'),
    ('sending', 'Отправление'),
    ('sent', 'Отправлено'),
    ('viewed', 'Просмотрено')
)


class WhatsappMessage(models.Model):
    message_id = models.CharField(max_length=75, verbose_name='ID')
    body = models.TextField(verbose_name='Текст')
    direction = models.CharField(max_length=3, verbose_name='Тип', choices=direction_choices)
    lead = models.ForeignKey('Lead', on_delete=models.CASCADE, verbose_name='Лид')
    user = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Пользователь', blank=True, null=True)
    status = models.CharField(max_length=10, verbose_name='Статус', choices=status_choices)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta(object):
        app_label = 'main'
        ordering = ['created_at']
        db_table = 'whatsapp_messages'
        verbose_name = 'сообщение из whatsapp'
        verbose_name_plural = 'сообщения из whatsapp'
