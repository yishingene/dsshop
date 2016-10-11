from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from oscar.apps.catalogue.categories import create_from_breadcrumbs

from myapps.catalogue.models import Product, ProductAttribute, ProductClass, ProductCategory

import os
import csv

#text = open(os.path.join(settings.MEDIA_ROOT, '//'), 'rb').read()

#import os
#from django.conf import settings
#text = open(os.path.join(settings.MEDIA_ROOT, 'a.txt'), 'rb').read()


class Command(BaseCommand):

	def handle(self, *args, **options):

		help = 'automatiseer de aanmaak van de product catalogus'

		FILE_PATH = os.path.join(settings.MEDIA_ROOT, 'product_list')
		#FILE = os.path.join(FILE_PATH, 'ds_chassis.csv')
		FILE = os.path.join(FILE_PATH, 'DS_Onderdelen.csv')
		
		with open(FILE) as file:

			reader = csv.reader(file, delimiter=';')

			for row in reader:
				'''
				Stappenplan:
				1. Check 5de rij (= UPC): mag niet leeg zijn
				2. Check 2de rij: ? 'Category'
				3. Maak product aan
				'''

				# Stap 1: Check 2de rij op de naam 'CATEGORY'
				if row[1] == 'CATEGORY':

					#cat_string = create_from_breadcrumbs(row[1])

					print('category: %s' % row[1])

				else:
					if row[4] in (None, ''):
						print('deze rij (%s) heeft geen UPC -> ignore!' % reader.line_num)

						pass

					else:
						print('product: %s' % row[0])



				#if reader.line_num == 1:
				#	pass



					'''product_class_name = 'Onderdelen'
					product_class = ProductClass.objects.get(pk=1)

					item = Product()
					item.title="temm"
					item.upc='temmy'
					item.product_class = product_class

					item.save()

					# DIT IS DE MANIER OM EEN CATEGORIE (TREE) AAN TE MAKEN!
					cat_string = create_from_breadcrumbs('test mij>tweede>derde')

					# EN DIT IS DE MANIER OM EEN PRODUCT AAN EEN CATEGORIE TE LINKEN
					ProductCategory.objects.update_or_create(product=item, category=cat_string)'''


				'''title = row[0]
				upc = row[4]

				try: 
					item = Product.objects.get(upc=upc)
				except Product.DoesNotExist:
					item = Product()

					item.upc = upc
					item.title = title
					item.product_class = product_class

					print('new! %s' % item)

					item.save()'''

		self.stdout.write('--Het is gefixt!--')