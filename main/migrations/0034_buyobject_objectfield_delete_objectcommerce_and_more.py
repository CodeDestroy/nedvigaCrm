# Generated by Django 5.0 on 2024-08-10 06:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_alter_deal_broker_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avito_id', models.BigIntegerField(default=0, verbose_name='Avito ID')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка')),
                ('published', models.BooleanField(default=False, verbose_name='Опубликовано?')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Кто создал')),
            ],
            options={
                'verbose_name': 'вторичный объект',
                'verbose_name_plural': 'вторичные объекты',
                'db_table': 'buy_objects',
            },
        ),
        migrations.CreateModel(
            name='ObjectField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, verbose_name='Название поля')),
                ('value', models.TextField(verbose_name='Значение')),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.buyobject', verbose_name='Объект')),
            ],
            options={
                'verbose_name': 'параметры объявления у объекта',
                'verbose_name_plural': 'параметры объявлений у объектов',
                'db_table': 'object_field',
            },
        ),
        migrations.DeleteModel(
            name='ObjectCommerce',
        ),
        migrations.DeleteModel(
            name='ObjectFlat',
        ),
        migrations.DeleteModel(
            name='ObjectHouse',
        ),
        migrations.DeleteModel(
            name='ObjectLease',
        ),
        migrations.AlterModelOptions(
            name='lead',
            options={'ordering': ['-pk'], 'verbose_name': 'лид', 'verbose_name_plural': 'лиды'},
        ),
        #migrations.AlterModelOptions(
        #    name='objectphoto',
        #    options={'verbose_name': 'фото объявления', 'verbose_name_plural': 'фотографии объявлений'},
        #),
        #migrations.AlterModelOptions(
        #    name='objectstat',
        #    options={'verbose_name': 'статистика по объекту', 'verbose_name_plural': 'статистика по объектам'},
        #),
    ]
