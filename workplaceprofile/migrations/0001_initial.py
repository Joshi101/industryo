# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0001_initial'),
        ('workplace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('industrial_area', models.CharField(null=True, blank=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'Asset',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('event', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('area', models.ForeignKey(to='workplaceprofile.Area')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('slug', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Material',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'operation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkplaceProfile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('address', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('about', models.TextField(null=True, blank=True)),
                ('points', models.IntegerField(default=0)),
                ('capabilities', models.TextField(null=True, blank=True, max_length=5000)),
                ('product_details', models.TextField(null=True, blank=True, max_length=5000)),
                ('Operation', models.ManyToManyField(to='workplaceprofile.Operation')),
                ('area', models.ForeignKey(to='workplaceprofile.Area', null=True)),
                ('assets', models.ManyToManyField(to='workplaceprofile.Asset')),
                ('institution', models.ForeignKey(to='workplaceprofile.Institution', null=True)),
                ('logo', models.ForeignKey(to='nodes.Images', null=True)),
                ('materials', models.ManyToManyField(to='workplaceprofile.Material')),
                ('participation', models.ManyToManyField(to='workplaceprofile.Events')),
                ('workplace', models.ForeignKey(to='workplace.Workplace')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
