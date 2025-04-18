# Generated by Django 5.0 on 2024-02-02 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_call_event_alter_call_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='flat_id',
        ),
        migrations.AddField(
            model_name='deal',
            name='complex_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='ID комплекса с сайта'),
        ),
        migrations.AddField(
            model_name='deal',
            name='complex_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Название комплекса с сайта'),
        ),
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Telegram ID'),
        ),
        migrations.AddField(
            model_name='user',
            name='telegram_username',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Telegram username'),
        ),
    ]
