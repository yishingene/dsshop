import logging

from oscar.apps.catalogue.views import CatalogueView as OscarCatalogueView

logger = logging.getLogger('oscar.catalogue')

class CatalogueView(OscarCatalogueView):

	def get_queryset(self):

		print( '------- MY CUSTOM VIEW')

		return super(CatalogueView, self).get_queryset()
