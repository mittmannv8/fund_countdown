# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-08 03:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cash_flow', '0016_cashinput_entry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashinput',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='inputs', to='cash_flow.Account'),
            preserve_default=False,
        ),
    ]
