from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from oscar.apps.catalogue.categories import create_from_breadcrumbs

from myapps.catalogue.models import Product, ProductAttribute, ProductClass, ProductCategory

import os
import csv

class Command(BaseCommand):

	def handle(self, *args, **options):

		help = 'automatiseer de aanmaak van de product catalogus'

		#FILE_PATH = os.path.join(settings.MEDIA_ROOT, 'product_list')
		FILE_PATH = settings.MEDIA_ROOT
		FILE = os.path.join(FILE_PATH, 'DS_Onderdelen.csv')
		
		with open(FILE) as file:

			reader = csv.reader(file, delimiter=';')

			cat_string = ''
			product_class = ProductClass.objects.get(pk=1)

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


		self.stdout.write('--Het is gefixt!--')