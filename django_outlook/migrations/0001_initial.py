# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0003_alter_email_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailHandler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=1024)),
                ('parameters', django_extensions.db.fields.json.JSONField()),
                ('auth', models.ForeignKey(to='default.UserSocialAuth')),
            ],
        ),
    ]
