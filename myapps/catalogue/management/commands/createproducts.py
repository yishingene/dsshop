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
		FILE = os.path.join(FILE_PATH, 'ds_chassis.csv')
		

		with open(FILE) as file:
			reader = csv.reader(file, delimiter=';')

			for row in reader:

				if reader.line_num == 1:

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


				title = row[0]
				upc = row[4]

				try: 
					item = Product.objects.get(upc=upc)
				except Product.DoesNotExist:
					item = Product()

					item.upc = upc
					item.title = title
					item.product_class = product_class

					print('new! %s' % item)

					item.save()

		self.stdout.write('--Het is gefixt!--')