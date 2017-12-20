# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20171214_1046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase_orders',
            old_name='order_no',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='items',
            name='PO',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='job',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notes',
            name='job',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scheduled_items',
            name='job',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shopping_list_items',
            name='job',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
