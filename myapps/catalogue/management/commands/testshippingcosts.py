from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import os

from oscar.apps.order.models import Order

class Command(BaseCommand):

	def handle(self, *args, **options):

		order_nr = 100101

		order = Order.objects.get(number=order_nr)

		order.shipping_excl_tax = 200.00
		order.shipping_incl_tax = 242.00

		order.save()

		print(order)

		self.stdout.write('--Het is gefixt!--')