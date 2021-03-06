# Generated by Django 3.1.6 on 2021-04-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_auto_20210410_0533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=250)),
                ('lga', models.CharField(max_length=250)),
                ('contact', models.CharField(max_length=250)),
                ('picture', models.ImageField(upload_to='home/hospital')),
                ('show', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='ocFbC', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='MJvmr', max_length=150),
        ),
    ]
