# Generated by Django 3.1.6 on 2021-04-03 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0015_auto_20210403_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='ahUleR', max_length=50),
        ),
    ]
