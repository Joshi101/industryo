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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('activity', models.CharField(choices=[('L', 'Like'), ('U', 'VoteUp'), ('D', 'VoteDown')], max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'activity',
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notification_type', models.CharField(choices=[('L', 'Liked'), ('C', 'Commented'), ('S', 'Also commented'), ('J', 'Also joined'), ('E', 'Edited'), ('U', 'VotedUp'), ('D', 'VotedDown'), ('A', 'Answered'), ('J', 'Joined')], max_length=1)),
                ('is_read', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
            bases=(models.Model,),
        ),
    ]
