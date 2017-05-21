from django.conf import settings

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






