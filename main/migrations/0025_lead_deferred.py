# Generated by Django 5.0 on 2024-05-20 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_user_return_to_list_alter_lead_warm'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='deferred',
            field=models.BooleanField(default=False, verbose_name='Отложенный спрос'),
        ),
    ]
