# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleTags',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='user/main')),
                ('image_thumbnail', imagekit.models.fields.ProcessedImageField(upload_to='user/thumbnails')),
                ('caption', models.CharField(max_length=255)),
                ('time', models.TimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=20, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('category', models.CharField(choices=[('F', 'Feed'), ('A', 'Article'), ('C', 'Comment'), ('D', 'Dashboard')], default='F', max_length=1)),
                ('title', models.TextField(max_length=255, null=True, db_index=True, blank=True)),
                ('post', models.TextField(max_length=5000)),
                ('slug', models.SlugField(max_length=255, null=True, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comments', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('admin_score', models.FloatField(default=1)),
                ('score', models.FloatField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.ForeignKey(to='nodes.Images', null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, to='nodes.Node')),
                ('tags', models.ManyToManyField(to='tags.Tags', through='nodes.ArticleTags')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-score', '-date'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='articletags',
            name='article',
            field=models.ForeignKey(to='nodes.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articletags',
            name='tag',
            field=models.ForeignKey(to='tags.Tags'),
            preserve_default=True,
        ),
    ]
