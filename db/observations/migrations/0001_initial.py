# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 04:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataObservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, help_text='Enter observation date', verbose_name='Observation Date')),
                ('obsnum', models.CharField(choices=[('A', 'Observation A (first of two)'), ('B', 'Observation B (second of two)')], help_text='Is this the first or second observation?', max_length=1, verbose_name='Observation Index')),
            ],
            options={
                'verbose_name': 'Feedback observation',
                'verbose_name_plural': 'Feedback observations',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='short name', max_length=100)),
                ('description', models.CharField(blank=True, default='', help_text='extended description', max_length=5000)),
            ],
            options={
                'verbose_name': 'observation item',
                'verbose_name_plural': 'observation items',
            },
        ),
        migrations.CreateModel(
            name='MbMData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.IntegerField(help_text='How many minutes into the lesson is this observation?', verbose_name='Minute')),
                ('first10', models.TextField(blank=True, default='', verbose_name='First 10 seconds')),
                ('location', models.CharField(blank=True, choices=[('D', 'Desk'), ('S', 'Stationary'), ('M', 'Moving around room'), ('O', 'Out of room')], default='', max_length=2, verbose_name='Location')),
                ('rest', models.TextField(blank=True, default='', verbose_name='Rest of minute')),
                ('observation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to='observations.DataObservation')),
            ],
            options={
                'verbose_name': 'Minute by minute datum',
                'verbose_name_plural': 'Minute by minute data',
            },
        ),
        migrations.CreateModel(
            name='NumberedResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(choices=[(1, '1 (No evidence)'), (2, '2 (Little evidence)'), (3, '3 (Some evidence)'), (4, '4 (Lots of evidence)'), (5, '5 (Great deal of evidence)')], help_text='How much evidence of this item did you see', verbose_name='Score')),
                ('notes', models.TextField(blank=True, default='', verbose_name='Notes')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='observations.Item')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Observer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Obsform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Observation template',
                'verbose_name_plural': 'Observation templates',
            },
        ),
        migrations.CreateModel(
            name='ReviewObservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, help_text='Enter observation date', verbose_name='Observation Date')),
                ('obsnum', models.CharField(choices=[('A', 'Observation A (first of two)'), ('B', 'Observation B (second of two)')], help_text='Is this the first or second observation?', max_length=1, verbose_name='Observation Index')),
                ('observer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.Observer')),
            ],
            options={
                'verbose_name': 'Review observation',
                'verbose_name_plural': 'Review observations',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('region', models.CharField(choices=[('alice', 'Alice Springs'), ('barkly', 'Barkly')], max_length=50, verbose_name='Region')),
                ('remoteness', models.CharField(choices=[('urban', 'Urban'), ('remote', 'Remote'), ('vremote', 'Very Remote')], max_length=50, verbose_name='Remoteness')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('identifier', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Teacher Identifier')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.School', verbose_name="Teacher's School")),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='reviewobservation',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.Teacher'),
        ),
        migrations.AddField(
            model_name='numberedresult',
            name='observation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='observations.ReviewObservation'),
        ),
        migrations.AddField(
            model_name='item',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='observations.Obsform'),
        ),
        migrations.AddField(
            model_name='dataobservation',
            name='observer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.Observer'),
        ),
        migrations.AddField(
            model_name='dataobservation',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.Teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('name', 'description')]),
        ),
    ]
