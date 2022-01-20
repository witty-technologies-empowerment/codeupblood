# Generated by Django 3.1.6 on 2021-08-12 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_auto_20210812_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='location',
            field=models.TextField(blank=True, help_text='Enter bank address'),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='swift_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='eDsbv', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='JDIyI', max_length=150),
        ),
    ]