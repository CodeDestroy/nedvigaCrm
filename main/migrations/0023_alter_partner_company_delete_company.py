# Generated by Django 5.0 on 2024-05-07 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_alter_deal_sell_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='company',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Компания'),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
