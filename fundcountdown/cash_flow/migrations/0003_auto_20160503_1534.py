# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-03 15:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash_flow', '0002_auto_20160503_1521'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CashInput',
            new_name='Expense',
        ),
    ]
