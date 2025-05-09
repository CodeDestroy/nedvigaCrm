# Generated by Django 5.0 on 2024-09-02 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_remove_deal_broker_remove_deal_broker_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='bill_date',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='com_agent',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='com_get',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='com_get_date',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='com_manager',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='com_paid',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='com_status',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='planned_date',
        ),
        migrations.AlterField(
            model_name='deal',
            name='legal_status',
            field=models.CharField(blank=True, choices=[('consultation', 'Консультация'), ('collect_docs', 'Сбор документов'), ('deposit', 'Задаток'), ('closing_deal', 'Закрытие сделки')], max_length=15, null=True, verbose_name='Юридический статус'),
        ),
    ]
