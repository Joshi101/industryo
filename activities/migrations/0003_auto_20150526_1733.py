# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0001_initial'),
        ('activities', '0002_auto_20150526_1733'),
        ('forum', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='node',
            field=models.ForeignKey(blank=True, null=True, to='nodes.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='question',
            field=models.ForeignKey(blank=True, null=True, to='forum.Question'),
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
            field=models.ForeignKey(blank=True, null=True, to='forum.Answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='node',
            field=models.ForeignKey(blank=True, null=True, to='nodes.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='question',
            field=models.ForeignKey(blank=True, null=True, to='forum.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
