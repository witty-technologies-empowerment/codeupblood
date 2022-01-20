# Generated by Django 3.1.6 on 2021-08-12 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_auto_20210812_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='bankaccount',
            name='bank_name',
        ),
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='KHWTh', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='TSCym', max_length=150),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='bank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.bank'),
        ),
    ]
