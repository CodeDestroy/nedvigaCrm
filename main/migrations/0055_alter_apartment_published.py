# Generated by Django 5.1.5 on 2025-04-16 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_alter_apartment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='published',
            field=models.BooleanField(default=True, verbose_name='Публиковать в фид'),
        ),
    ]
