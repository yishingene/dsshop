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


class Command(BaseCommand):

	def handle(self, *args, **options):

		help = 'automatiseer het toevoegen van fotos aan een product'

		if settings.DEV:
			path = os.path.join(settings.MEDIA_ROOT + '/custom_image_list')

			for index, product in enumerate(Product.objects.all()):

				product_code = product.upc
				image_path = path + '/' + str(product_code) + '.jpg'

				try:
					img = open(image_path, 'r')

				except IOError: 
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
			path = os.path.join(settings.MEDIA_URL + 'custom_image_list')

			self.stdout.write('path: %s' % path)

			from boto.s3.connection import S3Connection
			from boto.s3.key import Key
			from boto.s3 import Object

			try:
				connection = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, host=settings.AWS_S3_HOST)

			except: 
				self.stdout.write('CONN PROBLEM')

			for index, product in enumerate(Product.objects.all()):

				product_code = product.upc
				image_path = path + '/' + str(product_code) + '.jpg'

				#self.stdout.write('product_code: %s' % product_code)
				#self.stdout.write('path: %s' % image_path)


				# image exists!
				#self.stdout.write('CONN OKE!')
				file_name = str(product_code) + '.jpg'

				bucket = connection.get_bucket('dsshop')
				key = Key(bucket, file_name)

				current_file = Object('dsshop', key)

				self.stdout.write('KEY: %s' % key)
				self.stdout.write('file??? %s' % current_file)


				# self.stdout.write('path: %s' % image_path)

				# if settings.DEV == True:
				# 	extended_path = 'file://' + image_path

				# else: 
				# 	extended_path = image_path

				# name = str(product_code) + '.jpg'

				# img_temp = NamedTemporaryFile(delete=True)
				# img_temp.write(urlopen(extended_path).read())
				# img_temp.flush()

				# new = ProductImage(product=product)

				# try:
				# 	new.original.save(name, File(img_temp), True)

				# except: 
				# 	print('BESTAAT REEDS')
				# 	continue

				# new.save()
				# print('SAVING')

			self.stdout.write('--Het is gefixt!--')



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

