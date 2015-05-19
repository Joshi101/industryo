# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='description',
            field=models.CharField(null=True, max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
