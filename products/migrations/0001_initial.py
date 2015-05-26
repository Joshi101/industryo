# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        ('nodes', '0002_auto_20150526_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('product', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('description', models.TextField(max_length=5000, blank=True, null=True)),
                ('image', models.ForeignKey(blank=True, null=True, to='nodes.Images')),
                ('tags', models.ManyToManyField(to='tags.Tags')),
            ],
            options={
                'db_table': 'Products',
            },
            bases=(models.Model,),
        ),
    ]
