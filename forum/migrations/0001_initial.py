# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('votes', models.IntegerField(default=0)),
                ('answer', models.TextField(max_length=5000)),
                ('time', models.TimeField(auto_now_add=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('images', models.ManyToManyField(to='nodes.Images')),
            ],
            options={
                'verbose_name': 'Answer',
                'ordering': ('-is_accepted', '-votes', 'time'),
                'verbose_name_plural': 'Answers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnswerComment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('comment', models.TextField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(to='forum.Answer')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Answer Comment',
                'ordering': ('time',),
                'verbose_name_plural': 'Answer Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(null=True, max_length=255)),
                ('question', models.TextField(max_length=5000)),
                ('votes', models.IntegerField(default=0)),
                ('time', models.TimeField(auto_now_add=True)),
                ('answered', models.BooleanField(default=False)),
                ('admin_score', models.IntegerField(default=1)),
                ('images', models.ManyToManyField(to='nodes.Images')),
            ],
            options={
                'verbose_name': 'Question',
                'ordering': ('-time',),
                'verbose_name_plural': 'Questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionComment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('comment', models.TextField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(to='forum.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Question Comment',
                'ordering': ('time',),
                'verbose_name_plural': 'Question Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionTags',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('question', models.ForeignKey(to='forum.Question')),
                ('tags', models.ForeignKey(to='tags.Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='tags.Tags', through='forum.QuestionTags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='forum.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
