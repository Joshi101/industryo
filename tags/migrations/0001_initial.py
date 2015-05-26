# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('tag', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('type', models.CharField(blank=True, null=True, max_length=50)),
                ('description', models.CharField(blank=True, null=True, max_length=255)),
                ('number', models.IntegerField(default=0)),
                ('logo', models.ForeignKey(blank=True, null=True, to='nodes.Images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
