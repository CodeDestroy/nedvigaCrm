from django.db import models

from . import CreatedUpdatedMixin


class Funnel(CreatedUpdatedMixin):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    def parent_stages(self):
        return self.stage_set.filter(parent=None)

    class Meta(object):
        app_label = 'main'
        db_table = 'funnels'
        verbose_name = 'воронка продаж'
        verbose_name_plural = 'воронки продаж'
