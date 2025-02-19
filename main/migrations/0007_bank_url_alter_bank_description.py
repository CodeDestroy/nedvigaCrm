# Generated by Django 5.0 on 2024-01-10 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_lead_surname'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на сайт'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]
