# Generated by Django 3.1.6 on 2021-03-18 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20210317_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='shrt_message',
            field=models.CharField(blank=True, max_length=145),
        ),
    ]