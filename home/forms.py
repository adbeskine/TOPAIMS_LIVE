from django import forms
from home.models import Jobs, Purchase_orders




class new_job_form(forms.Form):
	Name = forms.CharField(widget = forms.TextInput(attrs={'id':'Name'}))
	Email = forms.CharField(widget = forms.TextInput(attrs={'id':'Email'}))
	Phone = forms.CharField(widget = forms.TextInput(attrs={'id':'Phone'}))
	Address = forms.CharField(widget = forms.TextInput(attrs={'id':'Address'}))
	Note = forms.CharField(widget = forms.TextInput(attrs={'id':'Note'}))

class new_note_form(forms.Form):
	Title = forms.CharField(widget = forms.TextInput(attrs={'id':'Title_input'}))
	Text = forms.CharField(widget = forms.TextInput(attrs={'id':'Note_input'}))

class new_scheduled_item_form(forms.Form):
	description = forms.CharField(widget = forms.TextInput(attrs={'id':'schedule_item_name_input'}))
	date_1 = forms.DateField(widget = forms.SelectDateWidget(attrs={'id':'schedule_item_date_input_start'}))
	date_2 = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'schedule_item_date_input_finish'}))
	quantity = forms.IntegerField(widget = forms.NumberInput(attrs = {'id':'schedule_item_quantity_input'}))

class update_scheduled_item_date_form(forms.Form):
	update_date_1 = forms.DateField(widget = forms.SelectDateWidget(attrs={'id':'schedule_item_date_input_start'}))
	update_date_2 = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'schedule_item_date_input_finish'}))

class purchase_order_form(forms.Form):
	Supplier = forms.CharField(widget= forms.TextInput(attrs={'id':'supplier_input'}))
	Supplier_ref = forms.CharField(widget= forms.TextInput(attrs={'id':'supplier_ref_input'}))
	order_no = forms.ModelChoiceField(queryset=Purchase_orders.objects.all(), required=False, disabled=True)

	item_1_description = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_1_description_input'}))
	item_1_fullname = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_1_fullname_input'}))
	item_1_price = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_1_price_input'}))
	item_1_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False, widget = forms.Select(attrs={'id':'item_1_job_input'})) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_1_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False, widget= forms.Select(attrs={'id':'item_1_delivery_location_input'})) # make it a radio widget, see docs on widgets
	item_1_delivery_date = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'item_1_delivery_date_input'}))
	item_1_quantity = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_1_quantity_input'}))

	item_2_description = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_2_description_input'}))
	item_2_fullname = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_2_fullname_input'}))
	item_2_price = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_2_price_input'}))
	item_2_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False, widget = forms.Select(attrs={'id':'item_2_job_input'})) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_2_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False, widget= forms.Select(attrs={'id':'item_2_delivery_location_input'})) # make it a radio widget, see docs on widgets
	item_2_delivery_date = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'item_2_delivery_date_input'}))
	item_2_quantity = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_2_quantity_input'}))

	item_3_description = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_3_description_input'}))
	item_3_fullname = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_3_fullname_input'}))
	item_3_price = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_3_price_input'}))
	item_3_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False, widget = forms.Select(attrs={'id':'item_3_job_input'})) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_3_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False, widget= forms.Select(attrs={'id':'item_3_delivery_location_input'})) # make it a radio widget, see docs on widgets
	item_3_delivery_date = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'item_3_delivery_date_input'}))
	item_3_quantity = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_3_quantity_input'}))

	item_4_description = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_4_description_input'}))
	item_4_fullname = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_4_fullname_input'}))
	item_4_price = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_4_price_input'}))
	item_4_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False, widget = forms.Select(attrs={'id':'item_4_job_input'})) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_4_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False, widget= forms.Select(attrs={'id':'item_4_delivery_location_input'})) # make it a radio widget, see docs on widgets
	item_4_delivery_date = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'item_4_delivery_date_input'}))
	item_4_quantity = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_4_quantity_input'}))

	item_5_description = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_5_description_input'}))
	item_5_fullname = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_5_fullname_input'}))
	item_5_price = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_5_price_input'}))
	item_5_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False, widget = forms.Select(attrs={'id':'item_5_job_input'})) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_5_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False, widget= forms.Select(attrs={'id':'item_5_delivery_location_input'})) # make it a radio widget, see docs on widgets
	item_5_delivery_date = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'item_5_delivery_date_input'}))
	item_5_quantity = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_5_quantity_input'}))

	item_6_description = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_6_description_input'}))
	item_6_fullname = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_6_fullname_input'}))
	item_6_price = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_6_price_input'}))
	item_6_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False, widget = forms.Select(attrs={'id':'item_6_job_input'})) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_6_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False, widget= forms.Select(attrs={'id':'item_6_delivery_location_input'})) # make it a radio widget, see docs on widgets
	item_6_delivery_date = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'item_6_delivery_date_input'}))
	item_6_quantity = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_6_quantity_input'}))

	item_7_description = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_7_description_input'}))
	item_7_fullname = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_7_fullname_input'}))
	item_7_price = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_7_price_input'}))
	item_7_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False, widget = forms.Select(attrs={'id':'item_7_job_input'})) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_7_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False, widget= forms.Select(attrs={'id':'item_7_delivery_location_input'})) # make it a radio widget, see docs on widgets
	item_7_delivery_date = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'item_7_delivery_date_input'}))
	item_7_quantity = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_7_quantity_input'}))

	item_8_description = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_8_description_input'}))
	item_8_fullname = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_8_fullname_input'}))
	item_8_price = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_8_price_input'}))
	item_8_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False, widget = forms.Select(attrs={'id':'item_8_job_input'})) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_8_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False, widget= forms.Select(attrs={'id':'item_8_delivery_location_input'})) # make it a radio widget, see docs on widgets
	item_8_delivery_date = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'item_8_delivery_date_input'}))
	item_8_quantity = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_8_quantity_input'}))

	item_9_description = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_9_description_input'}))
	item_9_fullname = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_9_fullname_input'}))
	item_9_price = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_9_price_input'}))
	item_9_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False, widget = forms.Select(attrs={'id':'item_9_job_input'})) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_9_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False, widget= forms.Select(attrs={'id':'item_9_delivery_location_input'})) # make it a radio widget, see docs on widgets
	item_9_delivery_date = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'item_9_delivery_date_input'}))
	item_9_quantity = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_9_quantity_input'}))

	item_10_description = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_10_description_input'}))
	item_10_fullname = forms.CharField(required=False, widget = forms.TextInput(attrs={'id':'item_10_fullname_input'}))
	item_10_price = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_10_price_input'}))
	item_10_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False, widget = forms.Select(attrs={'id':'item_10_job_input'})) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_10_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False, widget= forms.Select(attrs={'id':'item_10_delivery_location_input'})) # make it a radio widget, see docs on widgets
	item_10_delivery_date = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'item_10_delivery_date_input'}))
	item_10_quantity = forms.IntegerField(required=False, widget = forms.NumberInput(attrs={'id':'item_10_quantity_input'}))


class new_shopping_list_item_form(forms.Form):
	description = forms.CharField(widget = forms.TextInput(attrs={'id':'shopping_list_description_input'}))
	quantity = forms.IntegerField(widget = forms.NumberInput(attrs={'id':'shopping_list_quantity_input'}))
	job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", widget=forms.Select(attrs={'id':'shopping_list_job_input'}))

class reject_delivery_form(forms.Form):
	note = forms.CharField()
	reschedule_date = forms.DateField(required=False, widget=forms.SelectDateWidget)

class purchase_order_choice_form(forms.Form):
	purchase_order_number = forms.ModelChoiceField(queryset=Purchase_orders.objects.all(), to_field_name="order_no", widget=forms.Select(attrs={'id':'purchase_order_number_input'}))

class delete_job_form(forms.Form):
	job_deletion_selection = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address")
	security_field_1 = forms.CharField()
	security_field_2 = forms.CharField()