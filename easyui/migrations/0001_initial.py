# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easyui.mixins.model_mixins


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(help_text=b'\xe6\x9c\x80\xe5\xa4\x9a100\xe4\xb8\xaa\xe8\x8b\xb1\xe6\x96\x87\xe5\xad\x97\xe6\xaf\x8d\xe9\x95\xbf', max_length=100, verbose_name=b'\xe8\x8f\x9c\xe5\x8d\x95\xe5\x90\x8d')),
                ('is_root', models.BooleanField(default=False, help_text=b'\xe8\xbf\x99\xe4\xb8\xaa\xe4\xb8\x8d\xe6\xb7\xbb\xe7\x9a\x84\xef\xbc\x8cform\xe4\xb8\xad\xe7\xbc\xba\xe7\x9c\x81\xe5\xa4\x84\xe7\x90\x86', verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe4\xb8\xba\xe6\xa0\xb9\xe8\x8a\x82\xe7\x82\xb9')),
                ('parent_id', models.IntegerField(verbose_name=b'\xe7\x88\xb6ID')),
                ('namespace', models.CharField(max_length=100, verbose_name=b'APP\xe5\x90\x8d')),
                ('viewname', models.CharField(max_length=100, verbose_name=b'view\xe5\x90\x8d')),
                ('kwargs', models.CharField(max_length=100, verbose_name=b'\xe9\x99\x84\xe5\x8a\xa0\xe5\x8f\x82\xe6\x95\xb0')),
                ('is_system', models.BooleanField(default=False, help_text=b'\xe7\xb3\xbb\xe7\xbb\x9f\xe8\x8f\x9c\xe5\x8d\x95\xe5\x8f\xaa\xe5\xaf\xb9\xe8\xb6\x85\xe7\xba\xa7\xe7\x94\xa8\xe6\x88\xb7\xe5\x92\x8c\xe5\x90\x8e\xe5\x8f\xb0\xe7\x94\xa8\xe6\x88\xb7\xe6\x98\xbe\xe7\xa4\xba', verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe4\xb8\xba\xe7\xb3\xbb\xe7\xbb\x9f\xe8\x8f\x9c\xe5\x8d\x95')),
            ],
            options={
                'verbose_name': '\u83dc\u5355',
                'verbose_name_plural': '\u83dc\u5355',
            },
            bases=(easyui.mixins.model_mixins.ModelMixin, models.Model),
        ),
    ]
