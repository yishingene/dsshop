from django.core.management.base import BaseCommand, CommandError

from myapps.order.models import Order

class Command(BaseCommand):

	def handle(self, *args, **options):
		'''
		Set all stock to 1000
		'''

		for order in Order.objects.all():

			order.delete()

		self.stdout.write('--Het is gefixt!--')