from django.db import models


class BuyObject(models.Model):
    user = models.ForeignKey('User', verbose_name='Кто создал', on_delete=models.SET_NULL, null=True, blank=True)
    avito_id = models.BigIntegerField(verbose_name='Avito ID', default=0)
    url = models.CharField(verbose_name='Ссылка', max_length=255, null=True, blank=True)
    published = models.BooleanField(verbose_name='Опубликовано?', default=False)

    def __str__(self):
        fields = self.fields_for_list()
        return f'{fields["category"]} {fields["address"]}'

    def get_photos(self):
        from main.models.site import ObjectPhoto
        return ObjectPhoto.objects.filter(obj=self)

    def fields_for_list(self):
        fields = {'category':'', 'address':'', 'operation':'', 'price':''}
        if address := self.objectfield_set.filter(name='Address'):
            fields['address'] = address.first().value
        if category := self.objectfield_set.filter(name='Category'):
            fields['category'] = category.first().value
        if operation := self.objectfield_set.filter(name='OperationType'):
            fields['operation'] = operation.first().value
        if price := self.objectfield_set.filter(name='Price'):
            fields['price'] = price.first().value
        return fields

    class Meta(object):
        app_label = 'main'
        db_table = 'buy_objects'
        verbose_name = 'вторичный объект'
        verbose_name_plural = 'вторичные объекты'
