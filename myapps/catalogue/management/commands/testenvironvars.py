from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import os



class Command(BaseCommand):

	def handle(self, *args, **options):

		print(os.environ)
		print(os.environ['AWS_ACCESS_KEY_ID'])

		self.stdout.write('--Het is gefixt!--')