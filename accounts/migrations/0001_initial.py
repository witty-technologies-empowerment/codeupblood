# Generated by Django 3.1.6 on 2021-03-19 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('path', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
