# Generated by Django 3.1.6 on 2021-04-20 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0052_auto_20210414_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='LuAPpb', max_length=50),
        ),
    ]