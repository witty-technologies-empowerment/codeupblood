# Generated by Django 3.1.6 on 2021-04-09 18:04

from django.db import migrations, models
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_auto_20210409_1103'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tagulous_Blog_tags',
            new_name='Tagulous_Blog_tagz',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='tags',
        ),
        migrations.AddField(
            model_name='blog',
            name='tagz',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, help_text='Enter a comma-separated tag string', to='home.Tagulous_Blog_tagz'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='MhUgp', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='xUQFY', max_length=150),
        ),
    ]
