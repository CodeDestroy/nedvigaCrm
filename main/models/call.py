import asyncio

from channels.layers import get_channel_layer
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Модель полностью соответствует облачной атс дом ру 4.0 https://api.domru.biz/#/docs/crmapi/v1/general#description

directions = (
    ('in', 'Входящий'),
    ('out', 'Исходящий')
)

events = (
    ('INCOMING', 'Поступил звонок'),  # у менеджера должен начать звонить телефон в это время
    ('ACCEPTED', 'Сняли трубку (звонок принят)'),  # В этот момент можно убрать всплывающую карточку контакта в CRM.
    ('COMPLETED', 'Успешно завершен'),  # Менеджер или клиент положили трубку после разговора.
    ('CANCELLED', 'Звонок сброшен'),  # Клиент не дождался пока менеджер снимет трубку, либо если это был звонок на
                                      # группу менеджеров, на звонок мог ответить кто‑то еще.
    ('OUTGOING', 'Исходящий звонок'),  # Менеджер совершает исходящий звонок (ОАТС пытается дозвониться до клиента).
    ('TRANSFERRED', 'Переведен на другого')  # Звонок переведен на другого сотрудника.
)

statuses = (
    ('Success', 'Успешно'),  # Успешный звонок
    ('Missed', 'Пропущенный звонок'),  # пропущенный звонок
    ('Cancel', 'Звонок отменен'),  # звонок отменен
    # только исходящий
    ('Busy', 'Занято'),  # получен ответ «Занято»
    ('NotAvailable', 'Абонент недоступен'),  # получен ответ «Абонент недоступен»
    ('NotAllowed', 'Звонки на это направление запрещены'),  # получен ответ «Звонки на это направление запрещены»
    ('NotFound', 'Нет такого SIP-номера')  # получен ответ «Вызываемый абонент не найден, нет такого SIP номера»
)


class Call(models.Model):
    direction = models.CharField(max_length=4, choices=directions, verbose_name='Тип звонка')
    uuid = models.CharField(max_length=191, verbose_name='UUID', unique=True)
    status = models.CharField(max_length=13, choices=statuses, verbose_name='Статус звонка', null=True, blank=True)
    event = models.CharField(max_length=12, choices=events, verbose_name='Событие звонка', null=True, blank=True)
    record = models.CharField(max_length=255, verbose_name='Запись звонка', null=True, blank=True)
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')
    ext = models.CharField(max_length=15, verbose_name='Внутренний номер', null=True, blank=True)
    user = models.ForeignKey('User', verbose_name='Пользователь', on_delete=models.SET_NULL, null=True, blank=True)
    processed = models.BooleanField(default=False, verbose_name='Обработано')
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def get_card_template(self):
        return 'call/card.html'

    def lead(self):
        from main.models import Lead
        try:
            return Lead.objects.get(phone=self.phone)
        except ObjectDoesNotExist:
            return Lead.objects.get_or_create(phone=self.phone)[0]

    def get_event_text(self):
        match self.event:
            case 'INCOMING':
                return 'Поступил звонок'
            case 'ACCEPTED':
                return 'Сняли трубку (звонок принят)'
            case 'COMPLETED':
                return 'Успешно завершен'
            case 'CANCELLED':
                return 'Звонок сброшен'
            case 'OUTGOING':
                return 'Исходящий звонок'
            case 'TRANSFERRED':
                return 'Переведен на другого'
            case _:
                return '-'

    def get_status_text(self):
        match self.status:
            case 'Success':
                return 'Успешно'
            case 'Missed':
                return 'Пропущенный звонок'
            case 'Cancel':
                return 'Звонок отменен'
            case 'Busy':
                return 'Занято'
            case 'NotAvailable':
                return 'Абонент недоступен'
            case 'NotAllowed':
                return 'Звонки на это направление запрещены'
            case 'NotFound':
                return 'Нет такого SIP-номера'
            case _:
                return '-'

    class Meta(object):
        ordering = ['-created_at']
        app_label = 'main'
        db_table = 'calls'
        verbose_name = 'звонок'
        verbose_name_plural = 'звонки'


@receiver(post_save, sender=Call, dispatch_uid='create_update_call')
def create_update_call(instance, created, **kwargs):
    # Начало входящего звонка
    from main.models import Comment, Lead
    if instance.event == 'INCOMING':
        lead = instance.lead()
        channel_layer = get_channel_layer()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(channel_layer.group_send("call", {
            'type': 'show.call',
            'link': lead.get_absolute_url() if lead else '#',
            'name': lead.__str__() if lead else 'Новый клиент',
            'phone': instance.phone
        }))
    # Заранее получаем пользователя и сделку, используется почти везде
    if not (lead := Lead.objects.filter(phone=instance.phone).last()):
        lead = Lead.objects.create(phone=instance.phone, first_manager=instance.user)
    if instance.user and lead.responsible is None and instance.event == 'ACCEPTED':
        lead.responsible = instance.user
        lead.save()
        Comment.objects.create(
            type='lead',
            item_id=lead.pk,
            text=f'Добавлен при звонке пользователю: <b>{instance.user.last_name} {instance.user.first_name}</b>'
        )
    if lead.is_deleted:
        lead.is_deleted = False
        lead.save()
        Comment.objects.create(type='lead', item_id=lead.pk, text='Восстановлен из удаленных при звонке')
