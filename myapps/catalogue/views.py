import logging

from oscar.apps.catalogue.views import CatalogueView as OscarCatalogueView

from easy_pdf.views import PDFTemplateView

logger = logging.getLogger('oscar.catalogue')

class CatalogueView(OscarCatalogueView):

	def get_context_data(self, **kwargs):

		return super(CatalogueView, self).get_context_data(**kwargs)


class TestPdfView(PDFTemplateView):

	template_name = 'catalogue/pdf_test.html'
	download_filename = 'invoice_test.pdf'

	def get_context_data(self, **kwargs):
		return super(TestPdfView, self).get_context_data(pagesize='A4', title='Mijn titel!', **kwargs)