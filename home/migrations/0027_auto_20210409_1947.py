# Generated by Django 3.1.6 on 2021-04-10 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20210409_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='publish',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='WZppM', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='VbMYT', max_length=150),
        ),
    ]
