# Generated by Django 3.1.6 on 2021-04-20 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_survey_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='answer_ten',
            field=models.CharField(max_length=200),
        ),
    ]