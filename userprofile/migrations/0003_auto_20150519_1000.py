# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workplace', '0001_initial'),
        ('userprofile', '0002_auto_20150519_0913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='workplace',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='primary_workplace',
            field=models.ForeignKey(to='workplace.Workplace', null=True),
            preserve_default=True,
        ),
    ]
