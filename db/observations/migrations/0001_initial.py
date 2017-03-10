# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-03-07 04:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InteractionObservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('minutes', models.IntegerField(help_text='How long did you see the teacher doing this', verbose_name='Minutes')),
                ('evidenceDIPS', models.CharField(blank=True, default='', help_text='Examples: co-operative learning, student-generated questions', max_length=2000, verbose_name='Evidence of discursive interactions and power sharing strategies')),
                ('studentint', models.CharField(blank=True, choices=[('I', 'Indigenous or minoritised student'), ('O', 'Interaction with other student')], default='', help_text='Which students are the teacher interacting with?', max_length=1, verbose_name='Interactions with Students')),
                ('teacherloc', models.CharField(blank=True, default='', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('description', models.CharField(blank=True, default='', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='ItemObservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, help_text='Enter date or leave blank for current date and time', verbose_name='Observation Date and Time')),
                ('obsnum', models.CharField(choices=[('A', 'Observation A (first of two)'), ('B', 'Observation B (second of two)')], help_text='Is this the first or second observation?', max_length=1, verbose_name='Observation Index')),
            ],
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
        migrations.CreateModel(
            name='NumberedItemObservation',
            fields=[
                ('itemobservation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='observations.ItemObservation')),
                ('score', models.IntegerField(choices=[(1, '1 (No evidence)'), (2, '2 (Little evidence)'), (3, '3 (Some evidence)'), (4, '4 (Lots of evidence)'), (5, '5 (Great deal of evidence)')], help_text='How much evidence of this item did you see', verbose_name='Score')),
                ('notes', models.CharField(max_length=5000, verbose_name='Notes')),
            ],
            bases=('observations.itemobservation',),
        ),
        migrations.AddField(
            model_name='observation',
            name='observer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.Observer'),
        ),
        migrations.AddField(
            model_name='observation',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.Teacher'),
        ),
        migrations.AddField(
            model_name='itemobservation',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.Item'),
        ),
        migrations.AddField(
            model_name='itemobservation',
            name='observation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.Observation'),
        ),
    ]
