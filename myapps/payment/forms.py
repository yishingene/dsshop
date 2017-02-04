from django import forms

class HiddenOgoneForm(forms.Form):

	#def __init__(self, *args, **kwargs):


	amount = forms.IntegerField(widget=forms.HiddenInput())
	currency = forms.CharField(widget=forms.HiddenInput())
	language = forms.CharField(widget=forms.HiddenInput())
	order_id = forms.CharField(widget=forms.HiddenInput())
	psp_id = forms.CharField(widget=forms.HiddenInput())

	
