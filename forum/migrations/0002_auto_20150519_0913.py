# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='admin_score',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.SlugField(null=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.TextField(max_length=5000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(max_length=5000),
            preserve_default=True,
        ),
    ]
