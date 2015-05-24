# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(choices=[('L', 'Like'), ('U', 'VoteUp'), ('D', 'VoteDown')], max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('node', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Activities',
                'verbose_name': 'Activity',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notification_type', models.CharField(choices=[('L', 'Liked'), ('C', 'Commented'), ('S', 'Also commented'), ('K', 'Also joined'), ('E', 'Edited'), ('F', 'Follows'), ('U', 'VotedUp'), ('D', 'VotedDown')], max_length=1)),
                ('is_read', models.BooleanField(default=False)),
                ('answer', models.ForeignKey(to='forum.Answer')),
                ('from_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
                ('node', models.ForeignKey(to='nodes.Node')),
                ('question', models.ForeignKey(to='forum.Question')),
                ('to_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
            ],
            options={
                'verbose_name_plural': 'Notifications',
                'verbose_name': 'Notification',
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
    ]
