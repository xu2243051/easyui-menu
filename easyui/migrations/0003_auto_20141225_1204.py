# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import easyui.mixins.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('easyui', '0002_auto_20141223_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('menus_show', models.TextField(help_text=b'JSON\xe6\xa0\xbc\xe5\xbc\x8f\xe7\x9a\x84\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xef\xbc\x8c\xe5\x9c\xa8\xe8\x8f\x9c\xe5\x8d\x95\xe6\x98\xbe\xe7\xa4\xba', verbose_name=b'\xe8\x8f\x9c\xe5\x8d\x95\xe6\x98\xbe\xe7\xa4\xba\xe6\x9d\x83\xe9\x99\x90', blank=True)),
                ('menus_checked', models.TextField(help_text=b'JSON\xe6\xa0\xbc\xe5\xbc\x8f\xe7\x9a\x84\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2, checked\xe7\x94\xa8\xe6\x88\xb7\xe6\x9d\x83\xe9\x99\x90\xe9\x85\x8d\xe7\xbd\xae', verbose_name=b'\xe8\x8f\x9c\xe5\x8d\x95checked', blank=True)),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u83dc\u5355\u6743\u9650',
                'verbose_name_plural': '\u7528\u6237\u83dc\u5355\u6743\u9650',
            },
            bases=(easyui.mixins.model_mixins.ModelMixin, models.Model),
        ),
        migrations.AlterField(
            model_name='menu',
            name='is_system',
            field=models.BooleanField(default=False, help_text=b'\xe7\xb3\xbb\xe7\xbb\x9f\xe8\x8f\x9c\xe5\x8d\x95\xe5\x8f\xaa\xe5\xaf\xb9\xe8\xb6\x85\xe7\xba\xa7\xe7\x94\xa8\xe6\x88\xb7\xe5\x92\x8c\xe5\x90\x8e\xe5\x8f\xb0\xe7\x94\xa8\xe6\x88\xb7\xe6\x98\xbe\xe7\xa4\xba', verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe4\xb8\xba\xe7\xb3\xbb\xe7\xbb\x9f\xe8\x8f\x9c\xe5\x8d\x95', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='kwargs',
            field=models.CharField(max_length=100, verbose_name=b'\xe9\x99\x84\xe5\x8a\xa0\xe5\x8f\x82\xe6\x95\xb0', blank=True),
            preserve_default=True,
        ),
    ]
