from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings

from oscar.apps.catalogue.categories import create_from_breadcrumbs

from myapps.catalogue.models import Product, ProductAttribute, ProductClass, ProductCategory

import os
import csv
import urllib

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


class Command(BaseCommand):

	def handle(self, *args, **options):

		help = 'automatiseer de aanmaak van de product catalogus (voor onderdelen!)'

		FILE = os.path.join(settings.MEDIA_ROOT, '2cv_onderdelen.csv')
		
		with open(FILE) as file:

			reader = csv.reader(file, delimiter=';')
			product_class = ProductClass.objects.get(name='Onderdelen')

			for row in reader:
				'''STAPPENPLAN:
				1. Analyseer Product code (UPC), derde rij
				2. Maak product category aan als nog niet bestaat
				3. Maak product aan
				'''

				upc = str(row[2])

				if upc != '':

					if len(upc) == 6:

						car_type_id = upc[:1]
						category_id = upc[1:3]
						product_id = upc[-3:]

						if car_type_id == '2':

							main_cat = '2CV Onderdelen'

							if category_id == '13':
								cat_breadcrumb = 'Bumpers'

							else:
								continue

						else:
							continue

						cat_string = main_cat + '>' + cat_breadcrumb
						category = create_from_breadcrumbs(cat_string)

						try:
							product = Product.objects.get(upc=upc)

						except Product.DoesNotExist:

							product = Product()
							product.title = row[0]
							product.ucp = upc
							product.product_class = product_class

							product.save()

							ProductCategory.objects.update_or_create(product=product, category=category)

					else:
						continue

		self.stdout.write('--Het is gefixt!--')