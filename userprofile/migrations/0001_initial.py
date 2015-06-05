# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('workplace', '0001_initial'),
        ('tags', '0001_initial'),
        ('nodes', '0002_auto_20150604_1521'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('job_position', models.CharField(null=True, max_length=255)),
                ('experience', models.TextField(null=True, blank=True, max_length=5000)),
                ('points', models.IntegerField(default=100)),
                ('approved', models.BooleanField(default=True)),
                ('interests', models.ManyToManyField(to='tags.Tags')),
                ('primary_workplace', models.ForeignKey(null=True, to='workplace.Workplace')),
                ('profile_image', models.ForeignKey(null=True, blank=True, to='nodes.Images')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'userprofile',
            },
            bases=(models.Model,),
        ),
    ]
