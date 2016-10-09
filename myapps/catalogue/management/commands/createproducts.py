from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from myapps.catalogue.models import Product, ProductAttribute, ProductClass

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

			product_class_name = 'Onderdelen'
			product_class = ProductClass.objects.get(pk=1)

			for row in reader:

				title = row[0]
				upc = row[1]

				try: 
					item = Product.objects.get(upc=upc)
				except Product.DoesNotExist:
					item = Product()

					item.upc = upc
					item.title = title
					item.product_class = product_class

					print(item)

					item.save()

		self.stdout.write('--Het is gefixt!--')