# Generated by Django 3.1.6 on 2021-04-14 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0051_auto_20210414_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='x_status',
            field=models.CharField(default='pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='oEwHzz', max_length=50),
        ),
    ]
