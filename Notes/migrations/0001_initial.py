# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 12:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(default='', max_length=100)),
                ('Text', models.TextField(default='')),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('model', models.CharField(default='Notes', max_length=100)),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Jobs.Jobs')),
            ],
            options={
                'ordering': ('-Timestamp',),
            },
        ),
    ]
