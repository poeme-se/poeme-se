# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-30 10:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poemese', '0005_auto_20170430_0750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='profile_image',
        ),
    ]