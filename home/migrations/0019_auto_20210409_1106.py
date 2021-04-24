# Generated by Django 3.1.6 on 2021-04-09 18:06

from django.db import migrations, models
import tagulous.models.fields
import tagulous.models.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20210405_0730'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='flickr',
            new_name='instagram',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='linkedin',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='tags',
        ),
        migrations.AlterField(
            model_name='blog',
            name='author_picture',
            field=models.ImageField(upload_to='home/blog/author/image'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='partner',
            name='class_id',
            field=models.CharField(default='xptsv', max_length=150),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='class_id',
            field=models.CharField(default='jBXdS', max_length=150),
        ),
        migrations.CreateModel(
            name='Tagulous_Blog_tagz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.AddField(
            model_name='blog',
            name='tagz',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, help_text='Enter a comma-separated tag string', to='home.Tagulous_Blog_tagz'),
        ),
    ]
