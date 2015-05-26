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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('activity', models.CharField(choices=[('L', 'Like'), ('U', 'VoteUp'), ('D', 'VoteDown')], max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
                'db_table': 'activity',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notification_type', models.CharField(choices=[('L', 'Liked'), ('C', 'Commented'), ('S', 'Also commented'), ('J', 'Also joined'), ('E', 'Edited'), ('F', 'Follows'), ('U', 'VotedUp'), ('D', 'VotedDown')], max_length=1)),
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
