# Generated by Django 3.1.6 on 2021-04-09 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0026_auto_20210408_0347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='BMosNc', max_length=50),
        ),
    ]
