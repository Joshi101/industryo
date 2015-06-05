# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('email', models.EmailField(unique=True, verbose_name='e-mail address', max_length=75)),
                ('verified', models.BooleanField(default=False, verbose_name='verified')),
                ('primary', models.BooleanField(default=False, verbose_name='primary')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'email address',
                'verbose_name_plural': 'email addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('sent', models.DateTimeField(null=True, verbose_name='sent')),
                ('key', models.CharField(unique=True, verbose_name='key', max_length=64)),
                ('email_address', models.ForeignKey(to='account.EmailAddress', verbose_name='e-mail address')),
            ],
            options={
                'verbose_name': 'email confirmation',
                'verbose_name_plural': 'email confirmations',
            },
            bases=(models.Model,),
        ),
    ]
