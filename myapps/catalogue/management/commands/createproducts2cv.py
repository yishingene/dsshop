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

		help = 'automatiseer de aanmaak van de product catalogus'

		FILE = os.path.join(settings.MEDIA_ROOT, '2cv_onderdelen.csv')
		
		with open(FILE) as file:

			reader = csv.reader(file, delimiter=';')
			product_class = ProductClass.objects.get(name='Onderdelen')

			for row in reader:
				'''STAPPENPLAN:
				1. Analyseer Product code (UPC), derde rij
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

						print('CATEGORIE: %s' % cat_string)




						# print('CAR: %s' % car_type_id)
						# print('CAT: %s' % category_id)
						# print('PROD: %s' % product_id)

					else:
						continue


				'''
				Stappenplan:
				1. Check 5de rij (= UPC): mag niet leeg zijn
				2. Check 2de rij: ? 'Category'
				3. Maak product aan
				'''
				
				# Stap 1: Check 2de rij op de naam 'CATEGORY'
				# if row[1] == 'CATEGORY':

				# 	cat_string = create_from_breadcrumbs(row[0])

				# 	print('category: %s' % row[1])

				# # Stap 2: Als geen categorie, dan proberen we product aan te maken
				# else:
				# 	if row[4] in (None, ''):
				# 		print('deze rij (%s) heeft geen UPC -> ignore!' % reader.line_num)

				# 	else:
				# 		# Dit is een product!
				# 		print('product: %s -- %s' % (row[0], row[4]))

				# 		title = row[0]
				# 		upc = row[4]

				# 		try:
				# 			item = Product.objects.get(upc=upc)

				# 		except Product.DoesNotExist:

				# 			print('maak product aan')

				# 			# Maak product aan
				# 			item = Product()
				# 			item.title = title
				# 			item.upc = upc
				# 			item.product_class = product_class

				# 			item.save()

				# 			# Voeg categorie toe
				# 			ProductCategory.objects.update_or_create(product=item, category=cat_string)


		self.stdout.write('--Het is gefixt!--')