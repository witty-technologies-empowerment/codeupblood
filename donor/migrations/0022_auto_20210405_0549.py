# Generated by Django 3.1.6 on 2021-04-05 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0021_auto_20210405_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='qrLWiL', max_length=50),
        ),
    ]