from django.db import models


class CreatedUpdatedMixin(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Дата создания')
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Кто создал',
                                   related_name='%(class)s_created_items', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    updated_by = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Кто обновил',
                                   related_name='%(class)s_updated_items', blank=True, null=True)

    class Meta:
        abstract = True
