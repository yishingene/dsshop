from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings

from myapps.catalogue.models import Product, ProductImage

import os

class Command(BaseCommand):

	def handle(self, *args, **options):

		help = 'automatiseer het toevoegen van fotos aan een product'

		path = os.path.join(settings.MEDIA_ROOT + '/custom_image_list')

		for index, product in enumerate(Product.objects.all()):

			product_code = product.upc
			image_path = path + '/' + str(product_code) + '.jpg'

			#print('image: %s' % image_path)

			try:
				img = open(image_path, 'w')

			except: 
				print('EXCEPTION')
				continue

			print('--------------')

			print('img: %s' % img)

			image = File(img)

			# print('product code: %s' % product_code)
			# print('image: %s' % image_path)

			# new = ProductImage(product=product, original=image)

			# new.save()



		#print('MEDIA PATH: %s' % path)

		self.stdout.write('--Het is gefixt!--')






# import os
# >>> from django.conf import settings
# >>> initial_path = car.photo.path
# >>> car.photo.name = 'cars/chevy_ii.jpg'
# >>> new_path = settings.MEDIA_ROOT + car.photo.name
# >>> # Move the file on the filesystem
# >>> os.rename(initial_path, new_path)
# >>> car.save()
# >>> car.photo.path
# '/media/cars/chevy_ii.jpg'
# >>> car.photo.path == new_path
# True

# Zie ook: stackoverflow: programmatically saving image to django imagefield


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

