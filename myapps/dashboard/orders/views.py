from oscar.core.loading import get_class, get_model

from easy_pdf.views import PDFTemplateView

Order = get_model('order', 'Order')

class InvoicePdfView(PDFTemplateView):

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
		ctx['title'] = 'Dit is mijn titel'
		#ctx['order_nr'] = self.order_nr
		ctx['order'] = self.order

		return ctx






