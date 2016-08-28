# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedTask',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('task_name', models.CharField(db_index=True, max_length=255)),
                ('task_params', models.TextField()),
                ('task_hash', models.CharField(db_index=True, max_length=40)),
                ('priority', models.IntegerField(db_index=True, default=0)),
                ('run_at', models.DateTimeField(db_index=True)),
                ('attempts', models.IntegerField(db_index=True, default=0)),
                ('failed_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('last_error', models.TextField(blank=True)),
                ('locked_by', models.CharField(blank=True, db_index=True, max_length=64, null=True)),
                ('locked_at', models.DateTimeField(blank=True, db_index=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('task_name', models.CharField(db_index=True, max_length=255)),
                ('task_params', models.TextField()),
                ('task_hash', models.CharField(db_index=True, max_length=40)),
                ('priority', models.IntegerField(db_index=True, default=0)),
                ('run_at', models.DateTimeField(db_index=True)),
                ('attempts', models.IntegerField(db_index=True, default=0)),
                ('failed_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('last_error', models.TextField(blank=True)),
                ('locked_by', models.CharField(blank=True, db_index=True, max_length=64, null=True)),
                ('locked_at', models.DateTimeField(blank=True, db_index=True, null=True)),
            ],
            options={
                'db_table': 'background_task',
            },
            bases=(models.Model,),
        ),
    ]
