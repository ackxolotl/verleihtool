# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0003_auto_20170324_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='state',
            field=models.CharField(choices=[('1', 'pending'), ('2', 'approved'), ('3', 'declined'), ('4', 'revoked'), ('5', 'returned')], default='1', max_length=1),
        ),
    ]
