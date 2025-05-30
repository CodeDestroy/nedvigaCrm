# Generated by Django 5.0 on 2024-09-01 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_rename_size_mortgage_sum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='broker',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='broker_status',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='max_mortgage',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='mrtg',
        ),
        migrations.AddField(
            model_name='deal',
            name='legal_status',
            field=models.CharField(blank=True, choices=[('consultation', 'Консультация'), ('collect_docs', 'Сбор документов'), ('deposit', 'Задаток'), ('closing_deal', 'Закрытие сделки')], max_length=15, null=True, verbose_name='Ипотечный статус'),
        ),
    ]
