# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('comment', models.TextField(max_length=1000)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='main')),
                ('image_thumbnail', imagekit.models.fields.ProcessedImageField(upload_to='thumbnails')),
                ('time', models.TimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('anonymous', models.BooleanField(default=False)),
                ('w_type', models.CharField(max_length=1)),
                ('category', models.CharField(default='F', choices=[('F', 'Feed'), ('A', 'Article'), ('D', 'Dashboard')], max_length=1)),
                ('title', models.TextField(null=True, blank=True, max_length=255)),
                ('post', models.TextField(max_length=10000)),
                ('slug', models.SlugField(null=True, blank=True, max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('last_active', models.TimeField(auto_now=True)),
                ('comments_count', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('admin_score', models.FloatField(default=1)),
                ('score', models.FloatField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.ForeignKey(null=True, to='nodes.Images')),
            ],
            options={
                'ordering': ('-score', '-date'),
            },
            bases=(models.Model,),
        ),
    ]
