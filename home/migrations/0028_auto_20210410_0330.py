# Generated by Django 3.1.6 on 2021-04-10 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_auto_20210409_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='show',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='BCvZL', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='HMlGm', max_length=150),
        ),
    ]
