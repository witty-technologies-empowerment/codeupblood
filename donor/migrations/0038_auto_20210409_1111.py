# Generated by Django 3.1.6 on 2021-04-09 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0037_auto_20210409_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='RARyHS', max_length=50),
        ),
    ]