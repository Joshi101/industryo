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
            name='WorkplaceProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('area', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('about', models.TextField(null=True, blank=True)),
                ('points', models.IntegerField(default=0)),
                ('logo', models.ForeignKey(null=True, to='nodes.Images')),
                ('workplace', models.ForeignKey(to='workplace.Workplace')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
