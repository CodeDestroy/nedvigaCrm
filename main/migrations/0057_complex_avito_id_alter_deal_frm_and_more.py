# Generated by Django 5.1.5 on 2025-06-06 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_apartment_living_square'),
    ]

    operations = [
        migrations.AddField(
            model_name='complex',
            name='avito_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='frm',
            field=models.CharField(blank=True, choices=[('raz', 'Развитие'), ('nmarket', 'Нмаркет'), ('perv', 'Домклик'), ('vdk', 'ВДК'), ('new-code', 'Новый код'), ('sz-cube', 'СЗ куб'), ('contract', 'Прямой договор'), ('city', 'Сити-центр'), ('sec', 'Вторичка'), ('soy-dom', 'Свой дом'), ('pritazenie', 'Притяжение')], db_column='from', max_length=10, null=True, verbose_name='Через'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='developer',
            field=models.CharField(blank=True, choices=[('Collection', 'Коллекция'), ('Bobrov', 'Бобров')], max_length=50, null=True, verbose_name='Застройщик'),
        ),
    ]
