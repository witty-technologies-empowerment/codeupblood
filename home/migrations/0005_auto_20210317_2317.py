# Generated by Django 3.1.6 on 2021-03-18 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210317_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='current',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campaign',
            name='passed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campaign',
            name='upcoming',
            field=models.BooleanField(default=True),
        ),
    ]
