# Generated by Django 3.1.6 on 2021-04-08 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0024_auto_20210405_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='PQKIet', max_length=50),
        ),
    ]
