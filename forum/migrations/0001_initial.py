# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('votes', models.IntegerField(default=0)),
                ('answer', models.TextField(max_length=10000)),
                ('time', models.TimeField(auto_now_add=True)),
                ('is_accepted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-is_accepted', '-votes', 'time'),
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnswerComment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('comment', models.TextField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('time',),
                'verbose_name': 'Answer Comment',
                'verbose_name_plural': 'Answer Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('question', models.TextField(blank=True, null=True, max_length=5000)),
                ('votes', models.IntegerField(default=0)),
                ('answers', models.IntegerField(default=0)),
                ('time', models.TimeField(auto_now_add=True)),
                ('answered', models.BooleanField(default=False)),
                ('admin_score', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ('-time',),
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionComment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('comment', models.TextField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(to='forum.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('time',),
                'verbose_name': 'Question Comment',
                'verbose_name_plural': 'Question Comments',
            },
            bases=(models.Model,),
        ),
    ]
