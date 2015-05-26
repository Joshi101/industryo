# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        ('workplace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workplace',
            name='tags',
            field=models.ManyToManyField(to='tags.Tags'),
            preserve_default=True,
        ),
    ]
