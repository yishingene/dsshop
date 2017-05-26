import os

from django.views.generic import TemplateView, FormView, ListView, DetailView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
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

	def get_context_data(self, **kwargs):

		ctx = super(EventListView, self).get_context_data(**kwargs)

		for event in Event.objects.all():

			index = event.pk
			form_name = 'update_form_%s' % (index)
			ctx[form_name] = EventForm(instance=event)

		return ctx

	def post(self, request, *args, **kwargs):

		form = self.get_form()

		if form.is_valid():
			return self.form_valid(form)

		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		"""
		If the form is valid, redirect to the supplied URL.
		"""
		form.save(commit=True)

		return HttpResponseRedirect(self.success_url)

class EventDeleteView(DeleteView):

	model = Event
	success_url = reverse_lazy('event-list')

class EventUpdateView(FormView):

	model = Event
	success_url = reverse_lazy('event-list')
	fields = '__all__'
	form_class = EventForm
	queryset = None
	pk_url_kwarg = 'pk'


	def post(self, request, *args, **kwargs):

		print('------- post ')

		form = EventForm(request.POST, instance=self.get_object())

		if form.is_valid():
			return self.form_valid(form)

		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		"""
		If the form is valid, redirect to the supplied URL.
		"""
		self.object = form.save(commit=True)

		return HttpResponseRedirect(self.success_url)

	def get_object(self, queryset=None):

		if queryset is None:
			queryset = self.get_queryset()
		# Next, try looking up by primary key.
		pk = self.kwargs.get(self.pk_url_kwarg)

		if pk is not None:
			queryset = queryset.filter(pk=pk)
		# Next, try looking up by slug.
		
		# If none of those are defined, it's an error.
		if pk is None:
			raise AttributeError("Generic detail view %s must be called with "
		                     "an object pk"
		                     % self.__class__.__name__)
		try:
		# Get the single item from the filtered queryset
			obj = queryset.get()
		except queryset.model.DoesNotExist:
			raise Http404(_("No %(verbose_name)s found matching the query") %
		              {'verbose_name': queryset.model._meta.verbose_name})
		return obj

	def get_queryset(self):
	
		if self.queryset is None:
			if self.model:
				return self.model._default_manager.all()
			else:
				raise ImproperlyConfigured(
					"%(cls)s is missing a QuerySet. Define "
					"%(cls)s.model, %(cls)s.queryset, or override "
					"%(cls)s.get_queryset()." % {
					    'cls': self.__class__.__name__
					}
				)
		return self.queryset.all()

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

