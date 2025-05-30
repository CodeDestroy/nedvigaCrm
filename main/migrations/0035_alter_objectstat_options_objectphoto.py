# Generated by Django 5.0 on 2024-08-10 06:38

import django.db.models.deletion
import main.models.site.object_photo
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_buyobject_objectfield_delete_objectcommerce_and_more'),
    ]

    operations = [
        #migrations.AlterModelOptions(
        #    name='objectstat',
        #    options={'verbose_name': 'статистика по объекту', 'verbose_name_plural': 'статистика по объектам'},
        #),
        migrations.CreateModel(
            name='ObjectPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.FileField(help_text='Фото формата .png, .jpg, .jpeg. Не более 2мб', upload_to=main.models.site.object_photo.directory_path, verbose_name='Фото')),
                ('obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.buyobject', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'фото объявления',
                'verbose_name_plural': 'фотографии объявлений',
                'db_table': 'object_photo',
            },
        ),
    ]
