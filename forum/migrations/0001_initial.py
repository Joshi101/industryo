# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nodes', '0001_initial'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('votes', models.IntegerField(default=0)),
                ('answer', models.TextField()),
                ('time', models.TimeField(auto_now_add=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('images', models.ManyToManyField(to='nodes.Images')),
            ],
            options={
                'ordering': ('-is_accepted', '-votes', 'time'),
                'verbose_name_plural': 'Answers',
                'verbose_name': 'Answer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnswerComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('comment', models.TextField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(to='forum.Answer')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('time',),
                'verbose_name_plural': 'Answer Comments',
                'verbose_name': 'Answer Comment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('question', models.TextField()),
                ('votes', models.IntegerField(default=0)),
                ('time', models.TimeField(auto_now_add=True)),
                ('answered', models.BooleanField(default=False)),
                ('images', models.ManyToManyField(to='nodes.Images')),
            ],
            options={
                'ordering': ('-time',),
                'verbose_name_plural': 'Questions',
                'verbose_name': 'Question',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('comment', models.TextField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(to='forum.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('time',),
                'verbose_name_plural': 'Question Comments',
                'verbose_name': 'Question Comment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionTags',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
