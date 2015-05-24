# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='answer',
            field=models.ForeignKey(null=True, blank=True, to='forum.Answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='question',
            field=models.ForeignKey(null=True, blank=True, to='forum.Question'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='answer',
            field=models.ForeignKey(null=True, blank=True, to='forum.Answer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='node',
            field=models.ForeignKey(null=True, blank=True, to='nodes.Node'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='question',
            field=models.ForeignKey(null=True, blank=True, to='forum.Question'),
            preserve_default=True,
        ),
    ]
