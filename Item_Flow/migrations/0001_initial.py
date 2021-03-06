# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 12:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=100)),
                ('fullname', models.CharField(default='', max_length=100)),
                ('delivery_location', models.CharField(default='', max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=1.0, max_digits=25)),
                ('status', models.CharField(default='', max_length=100)),
                ('order_date', models.CharField(default='', max_length=100)),
                ('delivery_date', models.CharField(default='', max_length=100)),
                ('quantity', models.IntegerField(default=1)),
                ('model', models.CharField(default='Items', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase_orders',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('supplier', models.CharField(default='', max_length=100)),
                ('supplier_ref', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Scheduled_items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=100)),
                ('date_1', models.DateField(default=django.utils.timezone.now)),
                ('date_2', models.DateField(default=models.DateField(default=django.utils.timezone.now))),
                ('quantity', models.IntegerField(default=1)),
                ('model', models.CharField(default='Scheduled_items', max_length=100)),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Jobs.Jobs')),
            ],
        ),
        migrations.AddField(
            model_name='items',
            name='PO',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Item_Flow.Purchase_orders'),
        ),
        migrations.AddField(
            model_name='items',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Jobs.Jobs'),
        ),
    ]
