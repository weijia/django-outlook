# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_outlook', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailhandler',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AddField(
            model_name='mailhandler',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2018, 6, 28, 4, 40, 38, 895000, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mailhandler',
            name='is_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='mailhandler',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2018, 6, 28, 4, 40, 44, 748000, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
    ]
