from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings

from sorl.thumbnail import get_thumbnail

from myapps.catalogue.models import Product, ProductImage

import os
import urllib
from urllib.request import urlopen

from psycopg2 import IntegrityError
from django.db.utils import IntegrityError as DjangoIntegrityError

import requests


class Command(BaseCommand):

	def handle(self, *args, **options):

		help = 'automatiseer het toevoegen van fotos aan een product'

		if settings.DEV:
			
			'''
			DIT IS DE DEV METHODE ###################################################################
			'''

			path = os.path.join(settings.MEDIA_ROOT + '/custom_image_list')

			for index, product in enumerate(Product.objects.all()):

				product_code = product.upc
				image_path = path + '/' + str(product_code) + '.jpg'

				try:
					img = open(image_path, 'r')

				except IOError: 
					print('IO ERROR')
					continue

				# image exists!
				extended_path = 'file://' + image_path

				name = str(product_code) + '.jpg'

				img_temp = NamedTemporaryFile(delete=True)
				img_temp.write(urlopen(extended_path).read())
				img_temp.flush()

				new = ProductImage(product=product)

				try:
					new.original.save(name, File(img_temp), True)

				except: 
					continue

				new.save()
				print('SAVING')

			self.stdout.write('--Het is gefixt!--')

		else:

			path = 'https://dsshop.s3.eu-central-1.amazonaws.com/media/custom_image_list'

			for index, product in enumerate(Product.objects.all()):

				product_code = product.upc
				file_name = str(product_code) + '.JPG'

				image_path = path + '/' + file_name

				try:
					myfile = urlopen(image_path)

				except:
					self.stdout.write('--ERROR: file bestaat wsl niet-- %s' % product_code)
					continue

				image_content = ContentFile(requests.get(image_path).content) 

				new_image = ProductImage(product=product)

				self.stdout.write('VERDER: %s' % product_code)

				try:
					new_image.original.save(file_name, image_content)

				except IntegrityError: 
					self.stdout.write('--DUPLICATE KEY--')
					continue

				except DjangoIntegrityError:
					self.stdout.write('--DUPLICATE KEY-- van django')
					continue

				new_image.save()
				self.stdout.write('--SAVING--')

			self.stdout.write('--Het is gefixt!--')
