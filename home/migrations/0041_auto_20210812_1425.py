# Generated by Django 3.1.6 on 2021-08-12 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0040_auto_20210812_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='currency',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='BSfew', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='mKvpB', max_length=150),
        ),
    ]
