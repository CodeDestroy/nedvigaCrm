from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')
    birth = models.DateField(verbose_name='День рождения', null=True, blank=True)
    sip = models.ForeignKey('Phone', on_delete=models.SET_NULL, verbose_name='SIP-номер', null=True, blank=True)
    funnel = models.ForeignKey('Funnel', on_delete=models.SET_NULL, verbose_name='Основная воронка',
                               blank=True, null=True)
    fired = models.BooleanField(default=False, verbose_name='Уволен?')
    return_to_list = models.BooleanField(default=False, verbose_name='Вернуть в список сортировки?')
    debetor = models.BooleanField(default=False, verbose_name='Может просматривать дебеторскую задолженность?')
    in_stat = models.BooleanField(default=True, verbose_name='Участвует в сделке?')
    broker = models.BooleanField(default=False, verbose_name='Ипотечный брокер?')
    can_be_responsible = models.BooleanField(default=True, verbose_name='Может быть ответственным?')
    can_change_exclusive_responsible = models.BooleanField(default=False, verbose_name='Может менять ответственных у вторички?')
    telegram_id = models.CharField(max_length=15, verbose_name='Telegram ID', null=True, blank=True)
    telegram_username = models.CharField(max_length=15, verbose_name='Telegram username', null=True, blank=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        if self.first_name or self.last_name:
            return f'{self.last_name} {self.first_name}'
        return self.email

    def get_absolute_url(self):
        return reverse('main:user-list')

    def get_funnel_link(self):
        if self.funnel:
            return reverse('main:funnel-page', kwargs={'funnel_id': self.funnel.pk, 'user_id': self.pk})
        from main.models import Funnel
        funnel = Funnel.objects.first()
        if funnel:
            return reverse('main:funnel-page', kwargs={'funnel_id': funnel.pk, 'user_id': self.pk})
        return None

    def get_role_name(self):
        if self.is_staff and self.is_superuser:
            return 'Супермен'
        elif self.is_staff:
            return 'Администратор'
        return 'Менеджер'

    class Meta(object):
        app_label = 'main'
        ordering = ['pk', 'fired']
        db_table = 'users'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
