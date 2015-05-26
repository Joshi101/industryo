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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='main')),
                ('image_thumbnail', imagekit.models.fields.ProcessedImageField(upload_to='thumbnails')),
                ('caption', models.CharField(max_length=255)),
                ('time', models.TimeField(auto_now_add=True)),
                ('slug', models.SlugField(null=True, max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('category', models.CharField(choices=[('F', 'Feed'), ('A', 'Article'), ('C', 'Comment'), ('D', 'Dashboard')], max_length=1, default='F')),
                ('title', models.TextField(blank=True, null=True, max_length=255, db_index=True)),
                ('post', models.TextField(max_length=10000)),
                ('slug', models.SlugField(blank=True, null=True, max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comments', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('admin_score', models.FloatField(default=1)),
                ('score', models.FloatField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('published', models.BooleanField(default=True)),
                ('image', models.ForeignKey(null=True, to='nodes.Images')),
                ('parent', models.ForeignKey(blank=True, null=True, to='nodes.Node')),
            ],
            options={
                'ordering': ('-score', '-date'),
            },
            bases=(models.Model,),
        ),
    ]
