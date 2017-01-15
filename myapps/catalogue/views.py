import logging

from oscar.apps.catalogue.views import CatalogueView as OscarCatalogueView

logger = logging.getLogger('oscar.catalogue')

class CatalogueView(OscarCatalogueView):

	def get_context_data(self, **kwargs):

		return super(CatalogueView, self).get_context_data(**kwargs)
