# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0002_auto_20150525_1324'),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='image',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='image_thumbnail',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.ForeignKey(to='nodes.Images', null=True, blank=True),
            preserve_default=True,
        ),
    ]
