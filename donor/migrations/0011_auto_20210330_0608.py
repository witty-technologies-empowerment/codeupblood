# Generated by Django 3.1.6 on 2021-03-30 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0010_auto_20210330_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='HEVSEd', max_length=50),
        ),
    ]