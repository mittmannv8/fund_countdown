# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-08 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash_flow', '0012_auto_20160507_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
