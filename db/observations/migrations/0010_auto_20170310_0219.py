# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-03-10 02:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0009_auto_20170310_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interactionobservation',
            name='observation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.Observation'),
        ),
    ]
