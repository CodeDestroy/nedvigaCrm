# Generated by Django 5.0 on 2024-09-30 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_remove_deal_bill_date_remove_deal_com_agent_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='showing',
            options={'ordering': ['date_to'], 'verbose_name': 'показ объекта', 'verbose_name_plural': 'показы объектов'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['date_to'], 'verbose_name': 'задача', 'verbose_name_plural': 'задачи'},
        ),
        migrations.AddField(
            model_name='user',
            name='can_change_exclusive_responsible',
            field=models.BooleanField(default=False, verbose_name='Может менять ответственных у вторички?'),
        ),
    ]
