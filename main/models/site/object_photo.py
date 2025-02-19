from django.db import models


def directory_path(instance, filename):
    return f'object/photos_{instance.obj.pk}/{filename}'


class ObjectPhoto(models.Model):
    obj = models.ForeignKey('BuyObject', on_delete=models.CASCADE, verbose_name='Объявление', null=True, blank=True)
    photo = models.FileField(verbose_name='Фото', upload_to=directory_path,
                             help_text='Фото формата .png, .jpg, .jpeg. Не более 2мб')

    class Meta(object):
        app_label = 'main'
        db_table = 'object_photo'
        verbose_name = 'фото объявления'
        verbose_name_plural = 'фотографии объявлений'
