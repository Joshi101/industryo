# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20150604_1521'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0001_initial'),
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='node',
            field=models.ForeignKey(null=True, blank=True, to='nodes.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='question',
            field=models.ForeignKey(null=True, blank=True, to='forum.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='to_user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='answer',
            field=models.ForeignKey(null=True, blank=True, to='forum.Answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='node',
            field=models.ForeignKey(null=True, blank=True, to='nodes.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='question',
            field=models.ForeignKey(null=True, blank=True, to='forum.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
