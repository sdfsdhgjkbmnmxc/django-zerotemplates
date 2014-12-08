# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpareImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'spares')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ZeroTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(help_text='Example: my_page.html', unique=True, max_length=120, verbose_name='template name', db_index=True)),
                ('path', models.CharField(default=b'', help_text='Example: /my-page/. Optional', max_length=200, verbose_name='path', blank=True)),
                ('content', models.TextField(default=b'', verbose_name='content', blank=True)),
                ('comments', models.CharField(default=b'', help_text='internal use only', max_length=4800, verbose_name='comments', blank=True)),
                ('content_type', models.CharField(default=b'text/html', max_length=50, verbose_name=b'Content-type', choices=[(b'text/html', b'text/html'), (b'text/plain', b'text/plain'), (b'text/xml', b'text/xml'), (b'text/css', b'text/css')])),
            ],
            options={
                'ordering': ('filename',),
                'verbose_name': 'template',
                'verbose_name_plural': 'templates',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='spareimage',
            name='zero_template',
            field=models.ForeignKey(to='zerotemplates.ZeroTemplate'),
            preserve_default=True,
        ),
    ]
