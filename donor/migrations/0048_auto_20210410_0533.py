# Generated by Django 3.1.6 on 2021-04-10 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0047_auto_20210410_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='HiXDEc', max_length=50),
        ),
    ]