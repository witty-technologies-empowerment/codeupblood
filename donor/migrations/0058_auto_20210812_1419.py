# Generated by Django 3.1.6 on 2021-08-12 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0057_auto_20210811_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='ZqsGsM', max_length=50),
        ),
    ]