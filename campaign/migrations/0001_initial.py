# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(max_length=300, blank=True)),
                ('title', models.CharField(max_length=200, verbose_name='title', blank=True)),
                ('content', tinymce.models.HTMLField(verbose_name='content', blank=True)),
                ('position', models.PositiveIntegerField(verbose_name='Campaign ID #')),
                ('slug', models.CharField(max_length=300)),
                ('redirect_uri', models.URLField(max_length=300, blank=True)),
                ('redirect_choice', models.BooleanField(default=False, verbose_name='redirect')),
                ('template_name', models.CharField(help_text="Example: 'flatpages/contact_page.html'. If this isn't provided, the system will use 'flatpages/default.html'.", max_length=70, verbose_name='template name', blank=True)),
                ('registration_required', models.BooleanField(default=False, help_text='If this is checked, only logged-in users will be able to view the page.', verbose_name='registration required')),
                ('sites', models.ManyToManyField(to='sites.Site')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='campaign',
            unique_together=set([('user', 'slug')]),
        ),
    ]
