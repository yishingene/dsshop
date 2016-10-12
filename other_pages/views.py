from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _

from .forms import UploadFileForm

# Create your views here.
class ContactPageView(TemplateView):

	template_name = 'contact.html'

	def get_context_data(self, **kwargs):

		ctx = super(ContactPageView, self).get_context_data(**kwargs)
		ctx['page_title'] = _('contact')

		return ctx

class UploadView(FormView):

	template_name = 'others/upload.html'
	form_class = UploadFileForm

	def post(self, request, *args, **kwargs):

		print(request.FILES['file'])

		return super(UploadView, self).post(request, *args, **kwargs)


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

