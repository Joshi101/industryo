# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0002_auto_20150611_1315'),
        ('workplace', '0001_initial'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('product', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('image', models.ForeignKey(blank=True, to='nodes.Images', null=True)),
                ('producer', models.ForeignKey(to='workplace.Workplace')),
                ('tags', models.ManyToManyField(to='tags.Tags')),
            ],
            options={
                'db_table': 'Products',
            },
            bases=(models.Model,),
        ),
    ]
