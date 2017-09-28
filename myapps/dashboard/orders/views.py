from django.conf import settings
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from oscar.apps.dashboard.orders.views import OrderDetailView as OscarOrderDetailView
from oscar.core.loading import get_class, get_model

from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin
from easy_pdf.rendering import render_to_pdf_response, render_to_pdf
from decimal import Decimal as D

Order = get_model('order', 'Order')
ShippingCostForm = get_class('myapps.dashboard.orders.forms', 'ShippingCostForm')


class InvoiceDownloadView(PDFTemplateResponseMixin, TemplateView):

	base_url = 'file://' + settings.STATIC_ROOT

	if settings.DEV:
		img_url = '/Users/timclaes/development/thinkmobile/2016/dsshop/dsshop/common_static/images/logo_new.png'

	else:
		img_url = 'https://s3.eu-central-1.amazonaws.com/dsshop/media/images/logo_new.png'

	template_name = 'dashboard/orders/invoice.html'
	download_filename =  'factuur_tom_verheyden.pdf'
	content_type = 'application/pdf'

	order = None

	'''
	KIJK MSS BEST HIER NAAR: https://github.com/dentemm/festival/blob/1d6793de172dd2d45099afdce8762e08d96b7bd2/home/views.py
	'''

	# def dispatch(self, request, *args, **kwargs):

	# 	order_nr = kwargs['number']
	# 	self.order = Order.objects.get(number=order_nr)

	# 	return super(InvoiceDownloadView, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):

		self.order = Order.objects.get(number=kwargs['number'])

		ctx = self.get_context_data()

		render_to_pdf(request=request, template=self.template_name, context=ctx, download_filename=self.download_filename)

		return super(InvoiceDownloadView, self).get(request, *args, **kwargs)



	def get_context_data(self, **kwargs):

		ctx = super(InvoiceDownloadView, self).get_context_data(**kwargs)

		ctx['pagesize'] = 'A4'
		ctx['order'] = self.order
		ctx['url'] = self.img_url

		return ctx


class InvoicePdfView(PDFTemplateView):

	base_url = 'file://' + settings.STATIC_ROOT

	if settings.DEV:
		img_url = '/Users/timclaes/development/thinkmobile/2016/dsshop/dsshop/common_static/images/logo.png'

	else:
		img_url = ''

	template_name = 'dashboard/orders/invoice.html'
	download_filename =  'factuur_tom_verheyden.pdf'

	order = None

	def get(self, request, *args, **kwargs):

		order_nr = kwargs['number']
		self.order = Order.objects.get(number=order_nr)

		return super(InvoicePdfView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):

		ctx = super(InvoicePdfView, self).get_context_data(**kwargs)

		ctx['pagesize'] = 'A4'
		ctx['order'] = self.order
		ctx['url'] = self.img_url

		return ctx

class OrderDetailView(OscarOrderDetailView):

	def post(self, request, *args, **kwargs):
		'''
		Override to process custom ShippingCostForm
		'''

		order = self.object = self.get_object()

		if 'shipping_excl_tax' in request.POST:

			form = ShippingCostForm(request.POST, instance=self.object)
			form.save(commit=False)

			return self.reload_page(success='De verzendkosten zijn toegevoegd!')

		if 'order_action' in request.POST:
			return self.handle_order_action(
				request, order, request.POST['order_action']
				)

		if 'line_action' in request.POST:
			return self.handle_line_action(
				request, order, request.POST['line_action']
				)

		return self.reload_page(error=_("No valid action submitted"))

	def get_context_data(self, **kwargs):
		ctx = super(OrderDetailView, self).get_context_data(**kwargs)
		
		# Add custom form to context
		ctx['shipping_cost_form'] = ShippingCostForm(instance=self.object)

		return ctx

	def reload_page(self, fragment=None, error=None, success=None):
		'''
		Method override so we can add and displa success messages next to error messages
		'''
		url = reverse('dashboard:order-detail',
		          	kwargs={'number': self.object.number})
		if fragment:
			url += '#' + fragment
		if error:
			messages.error(self.request, error)
		if success:
			messages.success(self.request, success)
		return HttpResponseRedirect(url)
