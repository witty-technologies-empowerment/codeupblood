# Generated by Django 3.1.6 on 2021-04-10 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0049_auto_20210410_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='GlegyU', max_length=50),
        ),
    ]
