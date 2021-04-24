# Generated by Django 3.1.6 on 2021-04-10 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_auto_20210409_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='username',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='job',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='location',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='place_work',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='ZUSRL', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='GApTC', max_length=150),
        ),
    ]
