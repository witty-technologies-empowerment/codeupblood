# Generated by Django 3.1.6 on 2021-04-09 18:18

from django.db import migrations, models
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_merge_20210409_1117'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tagulous_Blog_tagz',
            new_name='Tagulous_Blog_tags',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='tagz',
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, help_text='Enter a comma-separated tag string', to='home.Tagulous_Blog_tags'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='nYhGP', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='WUbrH', max_length=150),
        ),
    ]
