# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
                ('industrial_area', models.CharField(blank=True, null=True, max_length=50)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True, max_length=1000)),
                ('workplace_type', models.CharField(max_length=1)),
                ('slug', models.SlugField(max_length=255)),
                ('logo', models.ForeignKey(blank=True, null=True, to='nodes.Images')),
            ],
            options={
                'db_table': 'Segment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('workplace_type', models.CharField(choices=[('A', 'Large Scale Industry'), ('B', 'Small & Medium Scale Enterprise'), ('C', 'College Teams'), ('O', 'Others')], max_length=1)),
                ('verified', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=255)),
                ('area', models.ManyToManyField(to='workplace.Area')),
                ('segments', models.ManyToManyField(to='workplace.Segment')),
            ],
            options={
                'db_table': 'Workplace',
            },
            bases=(models.Model,),
        ),
    ]
