# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
        ('forum', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, to='forum.Answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='from_user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
