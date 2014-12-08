# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zerotemplates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='zerotemplate',
            name='use_wysiwyg',
            field=models.BooleanField(default=False, verbose_name='Use WYSIWG editor'),
            preserve_default=True,
        ),
    ]
