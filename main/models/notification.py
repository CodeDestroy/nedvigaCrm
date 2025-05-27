from django.conf import settings
from django.db import models

type_choices = (
    ('danger', 'Важно!'),
    ('warning', 'Предупреждение'),
    ('normal', 'Обычное'),
    ('success', 'Успешно')
)


class Notification(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    text = models.CharField(max_length=255, verbose_name='Описание')
    priority = models.CharField(max_length=8, choices=type_choices, default='normal', verbose_name='Тип')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Для кого')
    type = models.CharField(max_length=8, choices=settings.ITEM_TYPE_CHOICES, default='task',
                            verbose_name='Тип сущности')
    item_id = models.IntegerField(default=0, verbose_name='ID сущности')
    read = models.BooleanField(default=False, verbose_name='Прочитано?')
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Дата создания')
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Кто создал',
                                   related_name='%(class)s_created_items', blank=True, null=True)

    def get_obj(self):
        from django.core.exceptions import ObjectDoesNotExist
        from main.models import Lead, Deal, Task, Showing
        try:
            match self.type:
                case 'lead':
                    return Lead.objects.get(id=self.item_id)
                case 'deal':
                    return Deal.objects.get(id=self.item_id)
                case 'task':
                    return Task.objects.get(id=self.item_id)
                case 'showing':
                    return Showing.objects.get(id=self.item_id)
        except ObjectDoesNotExist:
            return None

    def get_type(self):
        match self.type:
            case 'lead':
                return 'Контакт'
            case 'deal':
                return 'Сделка'
            case 'task':
                return 'Задача'
            case 'showing':
                return 'Показ'

    class Meta(object):
        app_label = 'main'
        db_table = 'notifications'
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'
