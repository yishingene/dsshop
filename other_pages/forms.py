from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string


class UploadFileForm(forms.Form):

	new_file = forms.FileField()

class ContactForm(forms.Form):

	name = forms.CharField()
	message = forms.CharField(widget=forms.Textarea)
	phone = forms.CharField()
	email = forms.CharField()
	company = forms.CharField()

	def send_email(self):

		ctx = {}
		ctx['name'] = self.cleaned_data['name']
		ctx['message'] = self.cleaned_data['message']
		ctx['company'] = self.cleaned_data.get('company', 'geen bedrijf opgegeven')
		ctx['email'] = self.cleaned_data['email']
		ctx['phone'] = self.cleaned_data['phone']
		
		title = 'Contactformulier van website'
		msg_html = render_to_string('others/contact_form.html', ctx)
		msg_plain = 'niet html versie'
		to_addresses = ['',]
		from_adress = 'alfa@beta.gamma'

		send_mail(subject=title, message=msg_plain, from_email=from_adress, recipient_list=to_addresses, html_message=msg_html)
