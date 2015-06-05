# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialaccount',
            name='provider',
            field=models.CharField(choices=[('facebook', 'Facebook'), ('google', 'Google')], max_length=30, verbose_name='provider'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialapp',
            name='provider',
            field=models.CharField(choices=[('facebook', 'Facebook'), ('google', 'Google')], max_length=30, verbose_name='provider'),
            preserve_default=True,
        ),
    ]
