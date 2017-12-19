from django import forms


class new_note_form(forms.Form):
	Title = forms.CharField(widget = forms.TextInput(attrs={'id':'Title_input'}))
	Text = forms.CharField(widget = forms.TextInput(attrs={'id':'Note_input'}))



