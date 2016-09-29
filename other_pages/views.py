from django.views.generic import TemplateView

from django.utils.translation import ugettext as _

# Create your views here.
class ContactPageView(TemplateView):

	template_name = 'contact.html'

	def get_context_data(self, **kwargs):

		ctx = super(ContactPageView, self).get_context_data(**kwargs)
		ctx['page_title'] = _('contact')

		return ctx