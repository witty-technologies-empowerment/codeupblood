# Generated by Django 3.1.6 on 2021-04-05 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20210405_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='cwyZt', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='WLDKP', max_length=150),
        ),
    ]
