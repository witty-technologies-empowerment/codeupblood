# Generated by Django 3.1.6 on 2021-08-11 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_auto_20210807_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='zTXEl', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='IxhsH', max_length=150),
        ),
    ]