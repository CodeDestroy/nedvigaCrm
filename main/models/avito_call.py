from django.db import models


def directory_path(instance, filename):
    return f'avito_calls/{instance.pk}/{filename}'


class AvitoCall(models.Model):
    cabinet = models.CharField(verbose_name='Из какого кабинета', choices=(
        ('old', 'Вторичка'), ('new_1', 'Первичка 1'), ('new_2', 'Первичка 2')
    ), default='old', max_length=6)
    buyer_phone = models.CharField(verbose_name='Номер покупателя', max_length=15)
    call_id = models.IntegerField(default=0, verbose_name='ID звонка')
    call_time = models.DateTimeField(verbose_name='Время звонка') # 2024-01-02T14:30:21+03:00
    seller_phone = models.CharField(verbose_name='Номер продавца', max_length=15)
    talk = models.IntegerField(default=0, verbose_name='Длительность разговора')
    virtual_phone = models.CharField(verbose_name='Виртуальный номер', max_length=15)
    waiting = models.IntegerField(default=0, verbose_name='Длительность ожидания')
    rec_file = models.FileField(verbose_name='Запись разговора', upload_to=directory_path, null=True, blank=True)

    class Meta(object):
        app_label = 'main'
        db_table = 'avito_calls'
        verbose_name = 'звонок из авито'
        verbose_name_plural = 'звонки из авито'
