# Generated by Django 3.1.6 on 2021-04-14 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20210414_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='QVBMj', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='LdelI', max_length=150),
        ),
    ]