# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('anonymous', models.BooleanField(default=False)),
                ('votes', models.IntegerField(default=0)),
                ('comments_count', models.IntegerField(default=0)),
                ('answer', models.TextField(max_length=10000)),
                ('date', models.TimeField(auto_now_add=True)),
                ('score', models.FloatField(default=0)),
                ('admin_score', models.IntegerField(default=1)),
                ('last_active', models.TimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-votes', 'date'),
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('anonymous', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('question', models.TextField(null=True, blank=True, max_length=5000)),
                ('votes', models.IntegerField(default=0)),
                ('answers', models.IntegerField(default=0)),
                ('date', models.TimeField(auto_now_add=True)),
                ('answered', models.BooleanField(default=False)),
                ('admin_score', models.IntegerField(default=1)),
                ('score', models.FloatField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('last_active', models.TimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
            bases=(models.Model,),
        ),
    ]
