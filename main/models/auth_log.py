from django.db import models


class AuthLog(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    ip = models.CharField(max_length=15, verbose_name='IP-адрес последней авторизации')
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Дата создания')

    class Meta(object):
        app_label = 'main'
        db_table = 'authlogs'
        verbose_name = 'последняя авторизация'
        verbose_name_plural = 'последние авторизации'
