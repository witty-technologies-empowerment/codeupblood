# Generated by Django 3.1.6 on 2021-04-10 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_auto_20210410_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='jcMGN', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='hjYLF', max_length=150),
        ),
    ]
