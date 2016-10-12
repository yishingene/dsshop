from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import os



class Command(BaseCommand):

	def handle(self, *args, **options):

		
		self.stdout.write('--Het is gefixt!--')