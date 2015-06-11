# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workplace', '0001_initial'),
        ('nodes', '0002_auto_20150604_1521'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('product', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('description', models.TextField(null=True, blank=True, max_length=1000)),
                ('image', models.ForeignKey(null=True, blank=True, to='nodes.Images')),
                ('producer', models.ForeignKey(to='workplace.Workplace')),
                ('tags', models.ManyToManyField(to='tags.Tags')),
            ],
            options={
                'db_table': 'Products',
            },
            bases=(models.Model,),
        ),
    ]
