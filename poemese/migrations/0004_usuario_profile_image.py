# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-29 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poemese', '0003_auto_20170429_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='profile-images'),
        ),
    ]