import os

from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import UploadFileForm, ContactForm, EventForm
from .models import Event

# Create your views here.
class EventListView(FormView, ListView):

	template_name = 'events/event_list.html'
	model = Event
	form_class = EventForm
	success_url = reverse_lazy('event-list')


class EventDetailView(FormView, DetailView):

	template_name = 'events/event_detail.html'
	model = Event

class ContactPageView(FormView):

	template_name = 'contact.html'
	form_class = ContactForm


	def post(self, request, *args, **kwargs):

		self.success_url = request.META.get('HTTP_REFERER')

		return super(ContactPageView, self).post(request, *args, **kwargs)

	def form_valid(self, form):

		form.send_email()

		messages.add_message(self.request, messages.SUCCESS, _('Bedankt voor je bericht!'))

		return super(ContactPageView, self).form_valid(form)

	def get_context_data(self, **kwargs):

		ctx = super(ContactPageView, self).get_context_data(**kwargs)
		ctx['page_title'] = _('contact')

		return ctx

class UploadView(FormView):

	template_name = 'others/upload.html'
	form_class = UploadFileForm

	def post(self, request, *args, **kwargs):

		self.success_url = request.META.get('HTTP_REFERER')

		return super(UploadView, self).post(request, *args, **kwargs)

	def form_valid(self, form):

		file = self.request.FILES['new_file']

		path = default_storage.save(file.name, ContentFile(file.read()))

		return super(UploadView, self).form_valid(form)

def upload_file(request):

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
        
		if form.is_valid():
			print('success!')
			return HttpResponseRedirect('/success/url/')

		else: 
			print('form not valid!')
	else:
		form = UploadFileForm()

	return render(request, 'others/upload.html', {'form': form})

