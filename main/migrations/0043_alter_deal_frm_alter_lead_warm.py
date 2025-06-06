# Generated by Django 5.1.5 on 2025-02-06 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_alter_showing_options_alter_task_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='frm',
            field=models.CharField(blank=True, choices=[('raz', 'Развитие'), ('nmarket', 'Нмаркет'), ('perv', 'Домклик'), ('vdk', 'ВДК'), ('new-code', 'Новый код'), ('sz-cube', 'СЗ куб'), ('contract', 'Прямой договор'), ('city', 'Сити-центр'), ('sec', 'Вторичка')], db_column='from', max_length=10, null=True, verbose_name='Через'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='warm',
            field=models.CharField(blank=True, choices=[('hot', 'Горячий'), ('warm', 'Теплый'), ('cold', 'Холодный'), ('rent', 'Аренда'), ('not_client', 'Не клиент'), ('not_call', 'Не дозвонились'), ('not_actual', 'Не актуально')], max_length=11, null=True, verbose_name='Теплота'),
        ),
    ]
