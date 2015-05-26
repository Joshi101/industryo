# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        ('nodes', '0002_auto_20150526_1631'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workplace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], null=True, max_length=1)),
                ('job_position', models.CharField(null=True, max_length=255)),
                ('experience', models.TextField(blank=True, null=True, max_length=5000)),
                ('points', models.IntegerField(default=0)),
                ('approved', models.BooleanField(default=True)),
                ('area', models.ForeignKey(blank=True, null=True, to='workplace.Area')),
                ('interests', models.ManyToManyField(to='tags.Tags')),
                ('primary_workplace', models.ForeignKey(null=True, to='workplace.Workplace')),
                ('profile_image', models.ForeignKey(blank=True, null=True, to='nodes.Images')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'userprofile',
            },
            bases=(models.Model,),
        ),
    ]
