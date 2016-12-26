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

			path = 'https://dsshop.s3.eu-central-1.amazonaws.com/media/custom_image_list'


			for index, product in enumerate(Product.objects.all()):

				product_code = product.upc
				file_name = str(product_code) + '.jpg'

				image_path = path + '/' + file_name

				#print('image path: %s' % image_path)

				try:
					myfile = urlopen(image_path)

				except:
					self.stdout.write('--ERROR--')
					continue

				print('product: %s' % product)
				print('file name: %s' % file_name)
				print('myfile: %s' % myfile)
				print('path: %s' % image_path)
				

				img_temp = NamedTemporaryFile(delete=True)
				img_temp.write(urlopen(image_path).read())
				img_temp.flush()

				print('img_temp: %s' % img_temp)

				new_image = ProductImage(product=product)

				try:
					new_image.original.save(file_name, File(img_temp))

				except: 
					print('ERROR SAVING IMG')
					break

				new_image.save()
				print('SAVING')

			self.stdout.write('--Het is gefixt!--')

			
			# path = os.path.join(settings.MEDIA_ROOT + '/custom_image_list')

			# for index, product in enumerate(Product.objects.all()):

			# 	product_code = product.upc
			# 	image_path = path + '/' + str(product_code) + '.jpg'

			# 	try:
			# 		img = open(image_path, 'r')

			# 	except IOError: 
			# 		print('IO ERROR')
			# 		continue

			# 	# image exists!
			# 	extended_path = 'file://' + image_path

			# 	name = str(product_code) + '.jpg'

			# 	img_temp = NamedTemporaryFile(delete=True)
			# 	img_temp.write(urlopen(extended_path).read())
			# 	img_temp.flush()

			# 	new = ProductImage(product=product)

			# 	try:
			# 		new.original.save(name, File(img_temp), True)

			# 	except: 
			# 		continue

			# 	new.save()
			# 	print('SAVING')

			# self.stdout.write('--Het is gefixt!--')

		else:

			path = 'https://dsshop.s3.eu-central-1.amazonaws.com/media/custom_image_list'


			for index, product in enumerate(Product.objects.all()):

				product_code = product.upc
				image_path = path + '/' + str(product_code) + '.jpg'

				#print('image path: %s' % image_path)

				try:
					myfile = urlopen(image_path)

				except:
					#self.stdout.write('--ERROR--')
					continue

				#print('myfile: %s' % myfile)
				file_name = str(product_code) + '.jpg'

				img_temp = NamedTemporaryFile(delete=True)
				img_temp.write(urlopen(myfile).read())
				img_temp.flush()

				new = ProductImage(product=product)

				try:
					new.original.save(name, File(img_temp), True)

				except: 
					continue

				product.save()
				print('SAVING')

			self.stdout.write('--Het is gefixt!--')


			# from boto.s3.connection import S3Connection
			# from boto.s3.key import Key


			# connection = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, host=settings.AWS_S3_HOST)
			# bucket = connection.get_bucket('dsshop')
			# bucket_list = bucket.list()

			# for index, product in enumerate(Product.objects.all()):

			# 	product_code = product.upc
			# 	image_path = path + '/' + str(product_code) + '.jpg'

			# 	#self.stdout.write('product_code: %s' % product_code)
			# 	#self.stdout.write('path: %s' % image_path)


			# 	# image exists!
			# 	#self.stdout.write('CONN OKE!')
			# 	file_name = str(product_code) + '.jpg'

			# 	bucket = connection.get_bucket('dsshop')
			# 	bucket_list = bucket.list()

			# 	for item in bucket_list:
			# 		self.stdout.write('list item: %s' % item)

			# self.stdout.write('--Het is gefixt!--')



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

