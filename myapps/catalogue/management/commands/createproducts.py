from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from myapps.catalogue.models import Product, ProductAttribute

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
				print('row: %s' % row[0])


				'''new, created = Product.objects.get_or_create(
					title=row[0],
					#upc=row[1],
					)'''

				#print(created)


#		for product in Product.objects.all():

#			new, created = Product.objects.get_or_create(name=)

#			print('product: %s' % product)

		self.stdout.write('--Het is gefixt!--')