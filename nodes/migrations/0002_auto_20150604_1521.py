# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20150604_1521'),
        ('tags', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='tags',
            field=models.ManyToManyField(to='tags.Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='node',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='images',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='answer',
            field=models.ForeignKey(null=True, blank=True, to='forum.Answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='node',
            field=models.ForeignKey(null=True, blank=True, to='nodes.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='question',
            field=models.ForeignKey(null=True, blank=True, to='forum.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
