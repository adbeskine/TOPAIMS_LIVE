def convert_to_date(str_date, form='%Y-%m-%d'):
	dt = datetime.datetime.strptime(str_date, form)
	return dt.date()

def create_custom_job(self, name, email, phone, address, note):
	form_data = {
	'Name':name,
	'Email':email,
	'Phone':phone,
	'Address':address,
	'Note':note,
	}

	response = self.client.post(reverse('new_job_form'), form_data, follow=True)

def create_shopping_list_item(self, description, job, quantity=1, homepage=False):

	if homepage == True:
		new_shopping_list_item_data = {
  		'description':description,
  		'job':job.address,
  		'quantity':quantity
  		}

  		return self.client.post(reverse('shopping_list_create', kwargs={'function':'create_homepage'}), data=new_shopping_list_item_data, follow=True)

  	
  	elif homepage == False:
  		new_shopping_list_item_data = {
  			'description':description,
  			'job':job.address,
  			'quantity':quantity
  		}
  		self.client.post(reverse('shopping_list_create', kwargs={'function':'create'}), data=new_shopping_list_item_data, follow=True)

def create_acquired_shopping_list_item(self, description, quantity, job):

	self.create_shopping_list_item(description, quantity, job)
	shopping_list_item = Shopping_list_items.objects.filter(description=description).first()
	self.client.get(reverse('acquired', kwargs={'pk':shopping_list_item.pk}), follow=True)

def create_purchase_order(
	self, Supplier='Stark Industries', Supplier_ref='123',
	description1=None, fullname1=None, delivery_date1=None, quantity1=None, price1=None, job1=None, delivery_location1=None,
	description2=None, fullname2=None, delivery_date2=None, quantity2=None, price2=None, job2=None, delivery_location2=None,
	description3=None, fullname3=None, delivery_date3=None, quantity3=None, price3=None, job3=None, delivery_location3=None,
	description4=None, fullname4=None, delivery_date4=None, quantity4=None, price4=None, job4=None, delivery_location4=None,
	description5=None, fullname5=None, delivery_date5=None, quantity5=None, price5=None, job5=None, delivery_location5=None,
	description6=None, fullname6=None, delivery_date6=None, quantity6=None, price6=None, job6=None, delivery_location6=None,
	description7=None, fullname7=None, delivery_date7=None, quantity7=None, price7=None, job7=None, delivery_location7=None,
	description8=None, fullname8=None, delivery_date8=None, quantity8=None, price8=None, job8=None, delivery_location8=None,
	description9=None, fullname9=None, delivery_date9=None, quantity9=None, price9=None, job9=None, delivery_location9=None,
	description10=None, fullname10=None, delivery_date10=None, quantity10=None, price10=None, job10=None, delivery_location10=None,
	):
		
	PO_data = {
	'Supplier':Supplier,
	'Supplier_ref':Supplier_ref,
	'item_1_description':description1,
	'item_1_fullname':fullname1,
	'item_1_delivery_location':(delivery_location1,),
	'item_1_job':job1.address,
	'item_1_delivery_date':delivery_date1, #must be date object.
	'item_1_quantity':quantity1,
	'item_1_price':price1,
	}

	if description2:
		PO_data.update({
			'item_2_description':description2,
			'item_2_fullname':fullname2,
			'item_2_delivery_location':(delivery_location2,),
			'item_2_job':job2.address,
			'item_2_delivery_date':delivery_date2, #must be date object.
			'item_2_quantity':quantity2,
			'item_2_price':price2,
				})

	if description3:
		PO_data.update({
			'item_3_description':description3,
			'item_3_fullname':fullname3,
			'item_3_delivery_location':(delivery_location3,),
			'item_3_job':job3.address,
			'item_3_delivery_date':delivery_date3, #must be date object.
			'item_3_quantity':quantity3,
			'item_3_price':price3,
				})

	if description4:
		PO_data.update({
			'item_4_description':description4,
			'item_4_fullname':fullname4,
			'item_4_delivery_location':(delivery_location4,),
			'item_4_job':job4.address,
			'item_4_delivery_date':delivery_date4, #must be date object.
			'item_4_quantity':quantity4,
			'item_4_price':price4,
				})

	if description5:
		PO_data.update({
			'item_5_description':description5,
			'item_5_fullname':fullname5,
			'item_5_delivery_location':(delivery_location5,),
			'item_5_job':job5.address,
			'item_5_delivery_date':delivery_date5, #must be date object.
			'item_5_quantity':quantity5,
			'item_5_price':price5,
				})

	if description6:
		PO_data.update({
			'item_6_description':description6,
			'item_6_fullname':fullname6,
			'item_6_delivery_location':(delivery_location6,),
			'item_6_job':job6.address,
			'item_6_delivery_date':delivery_date6, #must be date object.
			'item_6_quantity':quantity6,
			'item_6_price':price6,
				})

	if description7:
		PO_data.update({
			'item_7_description':description7,
			'item_7_fullname':fullname7,
			'item_7_delivery_location':(delivery_location7,),
			'item_7_job':job7.address,
			'item_7_delivery_date':delivery_date7, #must be date object.
			'item_7_quantity':quantity7,
			'item_7_price':price7,
				})

	if description8:
		PO_data.update({
			'item_8_description':description8,
			'item_8_fullname':fullname8,
			'item_8_delivery_location':(delivery_location8,),
			'item_8_job':job8.address,
			'item_8_delivery_date':delivery_date8, #must be date object.
			'item_8_quantity':quantity8,
			'item_8_price':price8,
				})

	if description9:
		PO_data.update({
			'item_9_description':description9,
			'item_9_fullname':fullname9,
			'item_9_delivery_location':(delivery_location9,),
			'item_9_job':job9.address,
			'item_9_delivery_date':delivery_date9, #must be date object.
			'item_9_quantity':quantity9,
			'item_9_price':price9,
				})

	if description10:
		PO_data.update({
			'item_10_description':description10,
			'item_10_fullname':fullname10,
			'item_10_delivery_location':(delivery_location10,),
			'item_10_job':job10.address,
			'item_10_delivery_date':delivery_date10, #must be date object.
			'item_10_quantity':quantity10,
			'item_10_price':price10,
				})

	self.client.post(reverse('purchase_order_homepage'), data=PO_data, follow=True)

def create_purchase_order_item(self, description, fullname, delivery_date, Supplier='Stark Industries', Supplier_ref='123', quantity=1, price=1, job=Jobs.objects.first(), delivery_location='shop'):
	
	PO_data = {
	'Supplier':Supplier,
	'Supplier_ref':Supplier_ref,
	'item_1_description':description,
	'item_1_fullname':fullname,
	'item_1_delivery_location':(delivery_location,),
	'item_1_job':job.address,
	'item_1_delivery_date':delivery_date, #must be date object.
	'item_1_quantity':quantity,
	'item_1_price':price
	}

	self.client.post(reverse('purchase_order', kwargs={'job_id':job.job_id}), data=PO_data, follow=True)

def create_job_note(self, title, text, job):
	note_form_data = {
		'Title':title,
		'Text':text
	}
	self.client.post(reverse('new_note', kwargs={'job_id':job.job_id}), data=note_form_data, follow=True)

def create_admin_note(self, title, text):
	note_form_data = {
		'Title':title,
		'Text':text
	}
	self.client.post(reverse('new_note', kwargs={'job_id':'admin'}), data=note_form_data, follow=True)

def create_schedule_item(self, description, date_1, quantity, job, date_2=None):
		
	if date_2:	
		schedule_item_form_data = {
			'description':description,
			'date_1':date_1,
			'date_2':date_2,
			'quantity':quantity
			}

		return self.client.post(reverse('new_schedule_item', kwargs={'job_id':job.job_id}), data=schedule_item_form_data, follow=True)

	else:
		schedule_item_form_data = {
			'description':description,
			'date_1':date_1,
			'quantity':quantity
			}

		return self.client.post(reverse('new_schedule_item', kwargs={'job_id':job.job_id}), data=schedule_item_form_data, follow=True)

def update_job_status(self, job, status):

	response = self.client.get(reverse('update_job', kwargs={'status':status, 'job_id': job.job_id}), follow=True)
	self.assertRedirects(response, reverse('job', kwargs={'job_id': job_id}))

def update_schedule_item_date(self, schedule_item, date_1, date_2=None):

	if date_2 != None:
		return self.client.post(reverse('schedule_item', kwargs={'function':'update', 'pk':scheduled_item_1.pk}), data={'update_date_1':date_1, 'update_date_2':date_2})
	
	self.client.post(reverse('schedule_item', kwargs={'function':'update', 'pk':scheduled_item_1.pk}), data={'update_date_1':date_1})


def update_PO_supplier_ref(self, purchase_order, new_ref):

	self.client.post(reverse('update_PO_supplier_ref', kwargs={'pk':purchase_order.pk}), data={new_supplier_ref:str(new_ref)})

def mark_showroom(self, Item): 
	
	self.client.get(reverse('mark_showroom'), kwargs={'pk':Item.pk})

def mark_on_site(self, Item):

	self.client.get(reverse('mark_on_site'), kwargs={'pk':Item.pk})
	
def reject_and_reschedule_item(self, Item, note='.'):
	# rejects an item and reschedules it for three weeks time, depends on the 'convert_to_date' method

	original_delivery_date = convert_to_date(Item.delivery_date)
	new_delivery_date = original_delivery_date+relativedelta(days=3)

	data = {
		'reschedule_date' : new_delivery_date,
		'note': note
		}

	self.client.post(reverse('reject_delivery', kwargs={'pk':Item.pk}), data=data, follow=True) # is follow really needed here?

def reject_and_cancel_item(self, Item, note='.'):
	# this will reject and cancel an item

	data = {
		'note':note
		}

	self.client.post(reverse('reject_delivery', kwargs={'pk':Item.pk}), data=data, follow=True) # is follow really needed here?

def mark_shopping_list_item_acquired(self, sli):
	# marks a shopping list item as acquired

	self.client.get(reverse('acquired', kwargs={'pk':sli.pk}), follow=True)

def delete_job(self, job):
	data = {
		'job_deletion_selection':(job.address,),
		'security_field_1':job.address,
		'security_field_2':job.address,
		}

	self.client.post(reverse('delete_job'), data=data, follow=True)

def delete_schedule_item(self, schedule_item):

	self.client.get(reverse('schedule_item', kwargs={'function':'delete', 'pk':schedule_item.pk}), follow=True)


def delete_shopping_list_item(self, sli): # sli = shopping list item
	
	self.client.get(reverse('delete', kwargs={'model':'Shopping_list_items', 'pk':sli.pk}), follow=True)

def delete_acquired_shopping_list_item(self, asli):

	self.client.get(reverse('delete', kwargs={'model':'Acquired_Item', 'pk':asli.pk}), follow=True)

def delete_item(self, item):

	self.client.get(reverse('delete', kwargs={'model':'Items', 'pk':item.pk}))

def delete_note(self, note):

	self.client.get(reverse('delete', kwargs={'model':'Notes', 'pk':note.pk}), follow=True)
	