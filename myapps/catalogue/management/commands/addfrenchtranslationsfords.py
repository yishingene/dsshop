from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.core.files.base import ContentFile
from django.conf import settings
from django.db.utils import IntegrityError


from myapps.catalogue.models import Product 

import os
import csv
import requests
import urllib
from decimal import Decimal
from urllib.request import urlopen
from psycopg2 import IntegrityError as PG_IntegrityError

# production mode
TRANSLATIONSFILE_FILE = 'https://s3.eu-central-1.amazonaws.com/dsshop/media/ds_french.csv'

# development mode
if settings.DEV == True:
	TRANSLATIONSFILE_FILE = 'file://' + os.path.join(settings.MEDIA_ROOT, '2pk_frans.csv')


class Command(BaseCommand):

	def handle(self, *args, **options):
		'''
		Voeg de franse vertalingen toe aan de bestaande producten
		'''

		help = 'Add French translations to existing products'

		with urlopen(TRANSLATIONSFILE_FILE) as file:

			csv_file = file.read()
			reader = csv.reader(csv_file.decode('utf-8').splitlines(), delimiter=';')

			for row in reader:

				upc = str(row[0])

				if upc != '':

					try:
						product = Product.objects.get(upc=upc)
						
						product.title_fr = str(row[1])
						product.save()
						#self.stdout.write('Product: %s' % upc)
						#self.stdout.write('Frans: %s' % str(row[3]))

					except Product.DoesNotExist:

						self.stdout.write('Bestaat niet ... ')
						continue

		self.stdout.write('--Het is gefixt!--')


