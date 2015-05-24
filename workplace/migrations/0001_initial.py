# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('workplace_type', models.CharField(max_length=1)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
                'db_table': 'Segment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SegmentTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('segment', models.ForeignKey(to='workplace.Segment')),
            ],
            options={
                'db_table': 'SegmentTags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('workplace_type', models.CharField(choices=[('A', 'Large Scale Industry'), ('B', 'Small & Medium Scale Enterprise'), ('C', 'College Teams'), ('O', 'Others')], max_length=1)),
                ('verified', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=255)),
                ('segments', models.ManyToManyField(through='workplace.SegmentTags', to='workplace.Segment')),
            ],
            options={
                'db_table': 'Workplace',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='segmenttags',
            name='workplace',
            field=models.ForeignKey(to='workplace.Workplace'),
            preserve_default=True,
        ),
    ]
