# Generated by Django 3.1.6 on 2021-04-10 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0045_auto_20210409_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='KVNSiH', max_length=50),
        ),
    ]
