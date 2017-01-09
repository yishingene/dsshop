from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.core.files.base import ContentFile
from django.conf import settings

from oscar.apps.catalogue.categories import create_from_breadcrumbs

from myapps.catalogue.models import Product, ProductAttribute, ProductClass, ProductCategory, ProductImage

import os
import csv
import requests
import urllib
from urllib.request import urlopen
from psycopg2 import IntegrityError

# Zie ook: stackoverflow: programmatically saving image to django imagefield

IMAGES_PATH = 'https://dsshop.s3.eu-central-1.amazonaws.com/media/custom_image_list'

if settings.DEV == True:
	IMAGES_PATH = 'file://' + settings.MEDIA_ROOT + '/custom_image_list'

PRODUCTS_FILE = 'https://s3.eu-central-1.amazonaws.com/dsshop/media/2cv_onderdelen.csv'

#if settings.DEV == True:
#	PRODUCTS_FILE = os.path.join(settings.MEDIA_ROOT, '2cv_onderdelen.csv')

def add_image_to_product(product, category, alternate_id):

	# Voor 2PK onderdelen is de bestandnaam van de afbeelding niet de UPC, maar de andere code
	if category == '2CV Onderdelen':
		product_code = alternate_id

	else:
		product_code = product.upc

	file_name = str(product_code) + '.jpg'
	image_path = IMAGES_PATH + '/' + file_name

	try:
		myfile = urlopen(image_path)

	except:
		print('--ERROR: file bestaat wsl niet--')
		return 0

	if settings.DEV:
		image_content = ContentFile(myfile.read())

	else:
		image_content = ContentFile(requests.get(image_path).content) 

	new_image = ProductImage(product=product)

	try:
		new_image.original.save(file_name, image_content)

	except IntegrityError: 
		print('DUPLICATE KEY')
		return 0

	new_image.save()
	print('SAVING IMAGE')

class Command(BaseCommand):

	def handle(self, *args, **options):

		help = 'automatiseer de aanmaak van de product catalogus (voor onderdelen!)'
		
		with urlopen(PRODUCTS_FILE) as file:

			csv_file = file.read()

			reader = csv.reader(csv_file.decode('utf-8').splitlines(), delimiter=';')
			product_class = ProductClass.objects.get(name='Onderdelen')

			print('HHHHHHHHHHH')

			for row in reader:

				'''STAPPENPLAN:
				1. Analyseer Product code (UPC), derde rij
				2. Maak product category aan als nog niet bestaat
				3. Maak product aan
				4. Voeg afbeelding toe aan product
				'''

				upc = str(row[2])
				alternate_id = str(row[1])

				if upc != '':

					if len(upc) == 6:

						car_type_id = upc[:1]
						category_id = upc[1:3]
						product_id = upc[-3:]

						if car_type_id == '2':

							main_cat = '2CV Onderdelen'

							if category_id == '11':
								cat_breadcrumb = 'Chassis'

							elif category_id == '12':
								cat_breadcrumb = 'Sierstrips'						

							elif category_id == '13':
								cat_breadcrumb = 'Bumpers'

							elif category_id == '14':
								cat_breadcrumb = 'Voorvleugel'

							elif category_id == '15':
								cat_breadcrumb = 'Motorkap'

							elif category_id == '16':
								cat_breadcrumb = 'Deuren'

							elif category_id == '17':
								cat_breadcrumb = 'Dak'

							elif category_id == '18':
								cat_breadcrumb = 'Achtervleugel'

							elif category_id == '19':
								cat_breadcrumb = 'Kofferklep'

							elif category_id == '21':
								cat_breadcrumb = 'Ruiten'

							elif category_id == '22':
								cat_breadcrumb = 'Uitlaat'

							elif category_id == '23':
								cat_breadcrumb = 'Elektriciteit & Ontsteking'

							elif category_id == '24':
								cat_breadcrumb = 'Verlichting'

							elif category_id == '25':
								cat_breadcrumb = 'Motorkap'

							elif category_id == '26':
								cat_breadcrumb = 'Benzinesysteem'

							elif category_id == '27':
								cat_breadcrumb = 'Koeling & Verwarming'

							elif category_id == '28':
								cat_breadcrumb = 'Remmen'

							elif category_id == '30':
								cat_breadcrumb = 'Leidingen'

							elif category_id == '31':
								cat_breadcrumb = 'Koppeling'

							elif category_id == '32':
								cat_breadcrumb = 'Interieur'

							elif category_id == '33':
								cat_breadcrumb = 'Allerlei'

							elif category_id == '35':
								cat_breadcrumb = 'Stuurinrichting'

							elif category_id == '36':
								cat_breadcrumb = 'Aandrijving & Ophanging'

							elif category_id == '37':
								cat_breadcrumb = 'Accesoires'

							elif category_id == '38':
								cat_breadcrumb = 'Sloten'

							elif category_id == '39':
								cat_breadcrumb = 'Plaatwerk'

							elif category_id == '40':
								cat_breadcrumb = 'Banden'

							else:
								continue

						else:
							continue

						cat_string = main_cat + '>' + cat_breadcrumb
						category = create_from_breadcrumbs(cat_string)

						try:
							product = Product.objects.get(upc=upc)

						except Product.DoesNotExist:

							self.stdout.write('*** creating product starts here')

							product = Product()
							product.title = row[0]
							product.upc = upc
							product.product_class = product_class

							product.save()

							ProductCategory.objects.update_or_create(product=product, category=category)

						finally:
							self.stdout.write('*** Adding image to product starts here')

							add_image_to_product(product, main_cat, alternate_id)

					else:
						continue

		self.stdout.write('--Het is gefixt!--')
