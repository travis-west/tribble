# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-25 17:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20181025_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='assigned_to',
            field=models.ForeignKey(null='True', on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='users_app.User'),
        ),
    ]