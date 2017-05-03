# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 22:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mbminteraction',
            name='rest',
            field=models.TextField(blank=True, default='', verbose_name='Rest of minute'),
        ),
        migrations.AlterField(
            model_name='mbminteraction',
            name='first10',
            field=models.TextField(blank=True, default='', verbose_name='First 10 seconds'),
        ),
    ]