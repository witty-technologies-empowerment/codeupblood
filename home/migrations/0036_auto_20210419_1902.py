# Generated by Django 3.1.6 on 2021-04-20 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_auto_20210419_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='mIzki', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='bNcMW', max_length=150),
        ),
    ]
