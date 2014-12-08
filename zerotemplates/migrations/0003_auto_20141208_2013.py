# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zerotemplates', '0002_zerotemplate_use_wysiwyg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zerotemplate',
            name='use_wysiwyg',
            field=models.BooleanField(default=False, help_text='Press "Save" for apply', verbose_name='Use WYSIWG editor'),
        ),
    ]
