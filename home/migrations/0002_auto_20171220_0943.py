# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 09:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
    	('home', '0001_initial')
    	]

    database_operations = [
    	migrations.AlterModelTable('Site_info', '_Auth_site_info'),
    	migrations.AlterModelTable('Jobs', 'Jobs_jobs'),
    	migrations.AlterModelTable('Notes', 'Notes_notes'),
    	migrations.AlterModelTable('Scheduled_items', 'Item_Flow_scheduled_items'),
    	migrations.AlterModelTable('Purchase_orders', 'Item_Flow_purchase_orders'),
    	migrations.AlterModelTable('Items', 'Item_Flow_items'),
    	migrations.AlterModelTable('Shopping_list_items', 'Shopping_list_shopping_list_items')
    ]

    state_operations = [
    	migrations.DeleteModel('Site_info'),
    	migrations.DeleteModel('Jobs'),
    	migrations.DeleteModel('Notes'),
    	migrations.DeleteModel('Scheduled_items'),
    	migrations.DeleteModel('Purchase_orders'),
    	migrations.DeleteModel('Items'),
    	migrations.DeleteModel('Shopping_list_items')
    ]

    operations = [
    	migrations.SeparateDatabaseAndState(
    		database_operations=database_operations,
    		state_operations=state_operations)
    ]