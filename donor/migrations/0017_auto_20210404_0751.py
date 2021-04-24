# Generated by Django 3.1.6 on 2021-04-04 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0016_auto_20210403_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewDonor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=125)),
                ('expires', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AlterField(
            model_name='appointment',
            name='d_id',
            field=models.CharField(default='FbriXg', max_length=50),
        ),
    ]
