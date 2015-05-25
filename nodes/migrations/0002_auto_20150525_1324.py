# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='main'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='images',
            name='image_thumbnail',
            field=imagekit.models.fields.ProcessedImageField(upload_to='thumbnails'),
            preserve_default=True,
        ),
    ]
