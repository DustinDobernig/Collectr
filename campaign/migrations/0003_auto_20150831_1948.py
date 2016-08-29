# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_auto_20150831_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='uid',
            field=models.CharField(max_length=300, verbose_name='User ID#', blank=True),
        ),
    ]
