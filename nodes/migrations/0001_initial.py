# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleTags',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='user/main')),
                ('image_thumbnail', imagekit.models.fields.ProcessedImageField(upload_to='user/thumbnails')),
                ('caption', models.CharField(max_length=255)),
                ('time', models.TimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('category', models.CharField(default='F', max_length=1, choices=[('F', 'Feed'), ('A', 'Article'), ('C', 'Comment'), ('D', 'Dashboard')])),
                ('title', models.TextField(blank=True, db_index=True, null=True, max_length=255)),
                ('post', models.TextField()),
                ('slug', models.SlugField(blank=True, null=True, max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comments', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('admin_score', models.FloatField(default=1)),
                ('score', models.FloatField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.ForeignKey(null=True, to='nodes.Images')),
                ('parent', models.ForeignKey(null=True, blank=True, to='nodes.Node')),
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
