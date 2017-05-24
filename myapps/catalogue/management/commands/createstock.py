from django.core.management.base import BaseCommand, CommandError

from myapps.catalogue.models import Product
from myapps.partner.models import StockRecord, Partner


class Command(BaseCommand):

	def handle(self, *args, **options):
		'''
		Set all stock to 1000
		'''

		partner = Partner.objects.get(name='Eigen stock')
		partner_id = partner.pk

		for product in Product.objects.all():

			try:
				stock = StockRecord.objects.get(partner__id=partner_id, product__id=product.id)

			except StockRecord.DoesNotExist:
				continue

			except:
				print('******** %s' % product.id)
				continue

			stock.num_in_stock = 1000
			self.stdout.write('-Updating stock-')
			stock.save()

		self.stdout.write('--Het is gefixt!--')
