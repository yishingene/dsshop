from django import forms

class UploadFileForm(forms.Form):

	new_file = forms.FileField()

class ContactForm(forms.Form):

	name = forms.CharField()
	message = forms.CharField(widget=forms.Textarea)

	def send_email(self):
		pass 