from django import forms

class UploadFileForm(forms.Form):

	new_file = forms.FileField()