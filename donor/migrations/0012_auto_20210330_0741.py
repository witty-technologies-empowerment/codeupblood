# Generated by Django 3.1.6 on 2021-03-30 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0011_auto_20210330_0608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='SjGGcE', max_length=50),
        ),
    ]
