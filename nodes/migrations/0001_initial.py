# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='main')),
                ('image_thumbnail', imagekit.models.fields.ProcessedImageField(upload_to='thumbnails')),
                ('caption', models.CharField(max_length=255)),
                ('time', models.TimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=20, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('category', models.CharField(max_length=1, default='F', choices=[('F', 'Feed'), ('A', 'Article'), ('C', 'Comment'), ('D', 'Dashboard')])),
                ('title', models.TextField(max_length=255, blank=True, db_index=True, null=True)),
                ('post', models.TextField(max_length=10000)),
                ('slug', models.SlugField(max_length=255, blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comments', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('admin_score', models.FloatField(default=1)),
                ('score', models.FloatField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('published', models.BooleanField(default=True)),
                ('image', models.ForeignKey(to='nodes.Images', null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, to='nodes.Node')),
            ],
            options={
                'ordering': ('-score', '-date'),
            },
            bases=(models.Model,),
        ),
    ]
