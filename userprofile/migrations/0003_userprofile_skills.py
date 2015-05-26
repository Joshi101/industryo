# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workplaceprofile', '0001_initial'),
        ('userprofile', '0002_auto_20150525_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='skills',
            field=models.ManyToManyField(to='workplaceprofile.Operation'),
            preserve_default=True,
        ),
    ]
