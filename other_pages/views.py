import os

from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from .forms import UploadFileForm, ContactForm

# Create your views here.
class ContactPageView(FormView):

	template_name = 'contact.html'
	form_class = ContactForm


	def post(self, request, *args, **kwargs):

		self.success_url = request.META.get('HTTP_REFERER')

		return super(ContactPageView, self).post(request, *args, **kwargs)

	def form_valid(self, form):

		form.send_email()

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

