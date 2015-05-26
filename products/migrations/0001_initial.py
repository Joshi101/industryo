# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0002_auto_20150526_1631'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('product', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('description', models.TextField(max_length=5000, null=True, blank=True)),
                ('image', models.ForeignKey(null=True, blank=True, to='nodes.Images')),
                ('tags', models.ManyToManyField(to='tags.Tags')),
            ],
            options={
                'db_table': 'Products',
            },
            bases=(models.Model,),
        ),
    ]
