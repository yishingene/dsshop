from django.conf import settings

from oscar.apps.dashboard.orders.views import OrderDetailView as OscarOrderDetailView
from oscar.core.loading import get_class, get_model

from easy_pdf.views import PDFTemplateView

Order = get_model('order', 'Order')

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

		print('------------------- My Order Detail View')

		order = self.object = self.get_object()

		if 'order_action' in request.POST:
			return self.handle_order_action(
				request, order, request.POST['order_action']
				)

		if 'line_action' in request.POST:
			return self.handle_line_action(
				request, order, request.POST['line_action']
				)

		return self.reload_page(error=_("No valid action submitted"))

