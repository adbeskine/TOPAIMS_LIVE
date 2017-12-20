from django import forms
from Jobs.models import Jobs

class new_shopping_list_item_form(forms.Form):
	description = forms.CharField(widget = forms.TextInput(attrs={'id':'shopping_list_description_input'}))
	quantity = forms.IntegerField(widget = forms.NumberInput(attrs={'id':'shopping_list_quantity_input'}))
	job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", widget=forms.Select(attrs={'id':'shopping_list_job_input'}))