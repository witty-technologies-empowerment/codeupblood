# Generated by Django 3.1.6 on 2021-04-05 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0020_auto_20210405_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='AsAkyM', max_length=50),
        ),
    ]