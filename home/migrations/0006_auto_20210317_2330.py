# Generated by Django 3.1.6 on 2021-03-18 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20210317_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='author_picture',
            field=models.ImageField(upload_to='home/campaign/author/picture'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='picture',
            field=models.ImageField(upload_to='home/campaign/post'),
        ),
    ]