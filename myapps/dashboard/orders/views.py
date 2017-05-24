from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from oscar.apps.dashboard.orders.views import OrderDetailView as OscarOrderDetailView
from oscar.core.loading import get_class, get_model

from easy_pdf.views import PDFTemplateView
from decimal import Decimal as D

Order = get_model('order', 'Order')
ShippingCostForm = get_class('myapps.dashboard.orders.forms', 'ShippingCostForm')
	

class InvoicePdfView(PDFTemplateView):

	#if settings.DEV:
	#base_url = '/Users/timclaes/development/thinkmobile/2016/dsshop/dsshop/common_static'

	base_url = 'file://' + settings.STATIC_ROOT

	if settings.DEV:
		img_url = '/Users/timclaes/development/thinkmobile/2016/dsshop/dsshop/common_static/images/logo.png'

	else:
		img_url = ''

	template_name = 'dashboard/orders/invoice.html'
	download_filename =  'factuur_tom_verheyden.pdf'

	#order_nr = 0
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

		order = self.object = self.get_object()

		print('**** REQUEST POST: %s' % request.POST)

		if 'shipping_excl_tax' in request.POST:


			form = ShippingCostForm(request.POST, instance=self.object)

			print('---------- ORDERDETAILVIEW: FORM HANDLING')
			print(form)

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
		
		# my own form
		ctx['shipping_cost_form'] = ShippingCostForm(instance=self.object)

		return ctx

	def reload_page(self, fragment=None, error=None, success=None):
		url = reverse('dashboard:order-detail',
		          	kwargs={'number': self.object.number})
		if fragment:
			url += '#' + fragment
		if error:
			messages.error(self.request, error)
		if success:
			messages.success(self.request, success)
		return HttpResponseRedirect(url)
