# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workplace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workplace',
            name='address',
            field=models.CharField(max_length=255, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workplace',
            name='contact',
            field=models.CharField(max_length=255, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workplace',
            name='institution',
            field=models.ForeignKey(related_name='institution', blank=True, null=True, to='tags.Tags'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workplace',
            name='logo',
            field=models.ForeignKey(to='nodes.Images', blank=True, null=True),
            preserve_default=True,
        ),
    ]
