# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workplace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('status', models.CharField(choices=[('F', 'Following'), ('B', 'Blocked')], max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('created',),
                'verbose_name_plural': ('relationships',),
                'verbose_name': ('relationship',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], null=True, max_length=1)),
                ('job_position', models.CharField(null=True, max_length=255)),
                ('experience', models.TextField(null=True, blank=True)),
                ('points', models.IntegerField(default=0)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='user/main')),
                ('image_thumbnail', imagekit.models.fields.ProcessedImageField(upload_to='user/thumbnails')),
                ('follows', models.ManyToManyField(to='userprofile.UserProfile', through='userprofile.Relationship', related_name='related_to')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserWorkplace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('authenticated', models.BooleanField(default=False)),
                ('date_joined', models.TimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='userprofile.UserProfile')),
                ('workplace', models.ForeignKey(to='workplace.Workplace')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='workplace',
            field=models.ManyToManyField(to='workplace.Workplace', through='userprofile.UserWorkplace'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relationship',
            name='from_user',
            field=models.ForeignKey(to='userprofile.UserProfile', related_name='from_person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relationship',
            name='to_user',
            field=models.ForeignKey(to='userprofile.UserProfile', related_name='to_person'),
            preserve_default=True,
        ),
    ]
