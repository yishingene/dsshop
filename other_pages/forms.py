from django import forms
from django.core.mail import send_mail


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
		ctx['name'] = self.name
		ctx['message'] = self.message
		ctx['company'] = self.company
		ctx['email'] = self.email
		ctx['phone'] = self.phone
		
		title = 'Contactformulier van website'
		msg_html = render_to_string('templates/others/contact_form.html', 'context': ctx)
		mgs_plain = 'niet html versie'
		to_addresses = ['',]
		from_adress = 'alfa@beta.gamma'

		send_mail(subject=title, message=msg_plain, from_email=from_adress, recipient_list=to_addresses, html_message=msg_html)



from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

from datetime import datetime, timedelta

from filter_app.models import Module

class Command(BaseCommand):

	help = 'Adss end date for all festivals'

	def handle(self, *args, **options):

		for module in Module.objects.all():

			if module.time_to_next_swap == 574:

				message = 'De filter leeftijd van module %s van toestel %s wordt over 4 weken bereikt!' % (module.name, module.main_tool.name) 
				send_mail('Filter wissel over 4 weken!', message, 'filters@imec.thinkmobile.webfactional.com', ['tim.claes@live.be', ], fail_silently=False)


				print('nog 4 weken te gaan')
				self.stdout.write(self.style.SUCCESS('4weken!'))

			elif module.time_to_next_swap == 0:

				message = 'De filter leeftijd van module %s van toestel %s is VANDAAG bereikt!' % (module.name, module.main_tool.name) 
				send_mail('Filter leeftijd vervalt vandaag!', message, 'filters@imec.thinkmobile.webfactional.com', ['tim.claes@live.be', ], fail_silently=False)

				print('vandaag wisselen!!!')
				self.stdout.write(self.style.SUCCESS('nu!!!!'))

			else:
				pass

		self.stdout.write(self.style.SUCCESS('Done!'))