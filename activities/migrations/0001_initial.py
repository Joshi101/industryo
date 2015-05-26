# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('activity', models.CharField(max_length=1, choices=[('L', 'Like'), ('U', 'VoteUp'), ('D', 'VoteDown')])),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Activities',
                'verbose_name': 'Activity',
                'db_table': 'activity',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notification_type', models.CharField(max_length=1, choices=[('L', 'Liked'), ('C', 'Commented'), ('S', 'Also commented'), ('J', 'Also joined'), ('E', 'Edited'), ('F', 'Follows'), ('U', 'VotedUp'), ('D', 'VotedDown')])),
                ('is_read', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Notifications',
                'verbose_name': 'Notification',
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
    ]
