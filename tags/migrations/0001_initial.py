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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('tag', models.CharField(db_index=True, max_length=50)),
                ('type', models.CharField(null=True, blank=True, max_length=1)),
                ('slug', models.SlugField()),
                ('description', models.CharField(null=True, blank=True, max_length=500)),
                ('count', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('logo', models.ForeignKey(null=True, blank=True, to='nodes.Images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
