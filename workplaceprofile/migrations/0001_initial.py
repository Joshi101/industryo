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
            name='Events',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('event', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('area', models.ForeignKey(to='workplace.Area')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkplaceProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('address', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('about', models.TextField(blank=True, null=True)),
                ('points', models.IntegerField(default=0)),
                ('capabilities', models.TextField(max_length=5000, blank=True, null=True)),
                ('product_details', models.TextField(max_length=5000, blank=True, null=True)),
                ('institution', models.ForeignKey(to='workplaceprofile.Institution', null=True)),
                ('logo', models.ForeignKey(to='nodes.Images', null=True)),
                ('participation', models.ManyToManyField(to='workplaceprofile.Events')),
                ('workplace', models.ForeignKey(to='workplace.Workplace')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
