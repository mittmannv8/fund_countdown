# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-08 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cash_flow', '0022_inputcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashinput',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cash_flow.InputCategory'),
            preserve_default=False,
        ),
    ]
