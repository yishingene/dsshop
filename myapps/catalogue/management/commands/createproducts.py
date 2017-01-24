from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings

from oscar.apps.catalogue.categories import create_from_breadcrumbs

from myapps.catalogue.models import Product, ProductAttribute, ProductClass, ProductCategory
from myapps.partner.models import StockRecord, Partner

from oscar.apps.partner.importers import CatalogueImporter

import os
import csv
import urllib
from decimal import Decimal

# Zie ook: stackoverflow: programmatically saving image to django imagefield


def add_image_to_product(product, product_code):


	full_path = path + get_image_file_name(product_code)

	os.path.isfile()

#	result = urllib.urlretrieve(image_url)
#
#	product.image.save(
#		os.path.basename(self.url),
#		File(open(result[0]))
#	)
#
#	product.save()

def get_image_file_name(product_code):

	filename = str(product_code) + '.jpg'

	return filename


def add_partner_information(product, partner_code, price_purchase, price_sell):
	'''
	Deze methode voegt de prijsinformatie toe aan een product door gebruik te maken van de Partner app
	'''

	partner = Partner.objects.get_or_create(name='Eigen stock')

	price = price_sell	#.replace(',', '.')

	print('---- prijs %s' % price)

	if price != '':

		importer = CatalogueImporter(logger=None)

		importer._create_stockrecord(
			item=product,
			partner_name=partner[0],
			partner_sku=partner_code,
			price_excl_tax=price,
			num_in_stock=0,
			stats=None
			)

class Command(BaseCommand):

	def handle(self, *args, **options):

		help = 'automatiseer de aanmaak van de product catalogus'

		#FILE_PATH = os.path.join(settings.MEDIA_ROOT, 'product_list')	# live
		FILE_PATH = settings.MEDIA_ROOT								# development
		FILE = os.path.join(FILE_PATH, 'DS_Onderdelen.csv')

		PRODUCTS_FILE = 'https://s3.eu-central-1.amazonaws.com/dsshop/media/DS_Onderdelen.csv'
		
		with open(PRODUCTS_FILE) as file:

			reader = csv.reader(file, delimiter=';')

			cat_string = ''
			product_class = ProductClass.objects.get(name='Onderdelen')

			for row in reader:
				'''
				Stappenplan:
				1. Check 5de rij (= UPC): mag niet leeg zijn
				2. Check 2de rij: ? 'Category'
				3. Maak product aan
				'''
				
				# Stap 1: Check 2de rij op de naam 'CATEGORY'
				if row[1] == 'CATEGORY':

					cat_string = create_from_breadcrumbs(row[0])

					print('category: %s' % row[1])

				# Stap 2: Als geen categorie, dan proberen we product aan te maken
				else:
					if row[4] in (None, ''):
						print('deze rij (%s) heeft geen UPC -> ignore!' % reader.line_num)

					else:
						# Dit is een product!
						print('product: %s -- %s' % (row[0], row[4]))

						title = row[0]
						upc = row[4]

						alternate_id = ''
						price_purchase = 0
						
						price_in_table = row[6]
						price_adjusted = price_in_table.replace(',', '.')
						price_inc = Decimal(price_adjusted)
						price_excl = price_inc / Decimal('1.21')
						price_sell = round(price_excl, 2)


						try:
							item = Product.objects.get(upc=upc)

						except Product.DoesNotExist:

							print('maak product aan')

							# Maak product aan
							item = Product()
							item.title = title
							item.upc = upc
							item.product_class = product_class

							item.save()

							# Voeg categorie toe
							ProductCategory.objects.update_or_create(product=item, category=cat_string)

						finally:
							if item:

								add_partner_information(
									product=item, 
									partner_code=alternate_id, 
									price_purchase=price_purchase,
									price_sell=price_sell
									)


		self.stdout.write('--Het is gefixt!--')