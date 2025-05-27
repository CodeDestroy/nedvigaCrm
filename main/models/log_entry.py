from django.db import models


class UserLogEntry(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    content_type = models.ForeignKey('contenttypes.ContentType', models.SET_NULL, verbose_name='Тип сущности',
                                     blank=True, null=True)
    object_id = models.IntegerField(verbose_name='ID объекта', default=0)
    fields = models.JSONField(null=True, blank=True)
    action_flag = models.PositiveSmallIntegerField('Тип события', choices=(
        (1, 'Изменено'), (2, 'Удалено')), default=1)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Дата создания')


    class Meta(object):
        ordering = ['created_at']
        app_label = 'main'
        db_table = 'user_log_entry'
        verbose_name = 'событие'
        verbose_name_plural = 'события'
