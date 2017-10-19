from django import forms
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.forms.widgets import SelectDateWidget

from .models import Event


class EventForm(forms.ModelForm):

	date = forms.DateField(widget=SelectDateWidget())

	class Meta:
		model = Event
		fields = '__all__'


class UploadFileForm(forms.Form):

	new_file = forms.FileField()

class ContactForm(forms.Form):

	name = forms.CharField()
	message = forms.CharField(widget=forms.Textarea)
	phone = forms.CharField()
	email = forms.CharField()
	company = forms.CharField(required=False)

	def send_email(self):

		subject = 'Nieuwe contactformulier via website!' + ' van: ' + self.cleaned_data['email']
		receivers = ['info@tomverheyden.com', ]
		sender = 'info@tomverheyden.com'

		ctx = {}
		ctx['name'] = self.cleaned_data['name']
		ctx['message'] = self.cleaned_data['message']
		ctx['company'] = self.cleaned_data.get('company', 'geen bedrijf opgegeven')
		ctx['email'] = self.cleaned_data['email']
		ctx['phone'] = self.cleaned_data['phone']

		message = get_template('others/contact_form.html').render(ctx)
		msg = EmailMessage(subject, message, to=receivers, from_email=sender)
		msg.content_subtype = 'html'
		msg.send()
