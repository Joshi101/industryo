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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('votes', models.IntegerField(default=0)),
                ('answer', models.TextField(max_length=10000)),
                ('time', models.TimeField(auto_now_add=True)),
                ('is_accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Answers',
                'verbose_name': 'Answer',
                'ordering': ('-is_accepted', '-votes', 'time'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnswerComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('comment', models.TextField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Answer Comments',
                'verbose_name': 'Answer Comment',
                'ordering': ('time',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('question', models.TextField(max_length=5000, blank=True, null=True)),
                ('votes', models.IntegerField(default=0)),
                ('answers', models.IntegerField(default=0)),
                ('time', models.TimeField(auto_now_add=True)),
                ('answered', models.BooleanField(default=False)),
                ('admin_score', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'Questions',
                'verbose_name': 'Question',
                'ordering': ('-time',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('comment', models.TextField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(to='forum.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Question Comments',
                'verbose_name': 'Question Comment',
                'ordering': ('time',),
            },
            bases=(models.Model,),
        ),
    ]
