# Generated by Django 3.1.6 on 2021-04-05 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0023_auto_20210405_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='TsRTWi', max_length=50),
        ),
    ]
