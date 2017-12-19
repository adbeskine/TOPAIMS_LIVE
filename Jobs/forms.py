from django import forms
from Jobs.models import Jobs

class new_job_form(forms.Form):
	Name = forms.CharField(widget = forms.TextInput(attrs={'id':'Name'}))
	Email = forms.CharField(widget = forms.TextInput(attrs={'id':'Email'}))
	Phone = forms.CharField(widget = forms.TextInput(attrs={'id':'Phone'}))
	Address = forms.CharField(widget = forms.TextInput(attrs={'id':'Address'}))
	Note = forms.CharField(widget = forms.TextInput(attrs={'id':'Note'}))

class delete_job_form(forms.Form):
	job_deletion_selection = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", widget = forms.Select(attrs={'id':'delete_job_choice_input'}))
	security_field_1 = forms.CharField(widget = forms.TextInput(attrs={'id':'security_field_1'}))
	security_field_2 = forms.CharField(widget = forms.TextInput(attrs={'id':'security_field_2'}))

