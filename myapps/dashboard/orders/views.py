from oscar.core.loading import get_class, get_model

from easy_pdf.views import PDFTemplateView

Order = get_model('order', 'Order')

class InvoicePdfView(PDFTemplateView):

	template_name = 'dashboard/orders/invoice.html'
	download_filename =  'factuur_tom_verheyden.pdf'

	def get_context_data(self, **kwargs):

		ctx = super(TestPdfView, self).get_context_data(**kwargs)

		ctx['pagesize'] = 'A4'
		ctx['title'] = 'Dit is mijn titel'

		return ctx


	# def get(self, request, *args, **kwargs):

	# 	return super(InvoicePdfView, self).get(request, *args, **kwargs)




