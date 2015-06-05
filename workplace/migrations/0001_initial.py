# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('workplace_type', models.CharField(choices=[('A', 'Large Scale Industry'), ('B', 'Small & Medium Scale Enterprise'), ('C', 'College Teams'), ('O', 'Others')], max_length=1)),
                ('verified', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('about', models.TextField(null=True, blank=True)),
                ('points', models.IntegerField(default=0)),
                ('capabilities', models.TextField(null=True, blank=True, max_length=5000)),
                ('product_details', models.TextField(null=True, blank=True, max_length=5000)),
                ('institution', models.ForeignKey(related_name='institution', to='tags.Tags')),
                ('logo', models.ForeignKey(null=True, to='nodes.Images')),
                ('segments', models.ManyToManyField(related_name='segments', to='tags.Tags')),
                ('tags', models.ManyToManyField(to='tags.Tags')),
            ],
            options={
                'db_table': 'Workplace',
            },
            bases=(models.Model,),
        ),
    ]
