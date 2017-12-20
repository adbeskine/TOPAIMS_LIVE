# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=100)),
                ('job_id', models.CharField(default='', max_length=100, unique=True)),
                ('status', models.CharField(default='quote', max_length=100)),
            ],
        ),
    ]
