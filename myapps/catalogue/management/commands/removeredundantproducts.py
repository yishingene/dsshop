from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings

from myapps.catalogue.models import Product

import os

# Zie ook: stackoverflow: programmatically saving image to django imagefield

class Command(BaseCommand):

	def handle(self, *args, **options):

		for product in Product.objects.all():

			if product.upc == None or product.upc == '':
				product.delete()

		self.stdout.write('--Het is gefixt!--')