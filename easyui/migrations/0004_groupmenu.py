# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easyui.mixins.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('easyui', '0003_auto_20141225_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('menus_show', models.TextField(help_text=b'JSON\xe6\xa0\xbc\xe5\xbc\x8f\xe7\x9a\x84\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xef\xbc\x8c\xe5\x9c\xa8\xe8\x8f\x9c\xe5\x8d\x95\xe6\x98\xbe\xe7\xa4\xba', verbose_name=b'\xe8\x8f\x9c\xe5\x8d\x95\xe6\x98\xbe\xe7\xa4\xba\xe6\x9d\x83\xe9\x99\x90', blank=True)),
                ('menus_checked', models.TextField(help_text=b'JSON\xe6\xa0\xbc\xe5\xbc\x8f\xe7\x9a\x84\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2, \xe4\xbf\x9d\xe7\x95\x99\xe7\x94\xa8\xe6\x88\xb7\xe7\xbb\x84checked\xe5\x86\x85\xe5\xae\xb9', verbose_name=b'\xe8\x8f\x9c\xe5\x8d\x95checked', blank=True)),
                ('group', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe7\xbb\x84', to='auth.Group', unique=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u7ec4\u83dc\u5355\u6743\u9650',
                'verbose_name_plural': '\u7528\u6237\u7ec4\u83dc\u5355\u6743\u9650',
            },
            bases=(easyui.mixins.model_mixins.ModelMixin, models.Model),
        ),
    ]
