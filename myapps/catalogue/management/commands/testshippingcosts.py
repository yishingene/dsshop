from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from oscar.apps.order.models import Order

import os

from decimal import Decimal as D

class Command(BaseCommand):

	def handle(self, *args, **options):

		order_nr = 100099

		order = Order.objects.get(number=order_nr)

		tax_excl = D('200.00')
		tax_incl = D('242.00')

		order.shipping_excl_tax = tax_excl
		order.shipping_incl_tax = tax_incl

		order.total_excl_tax = order.total_excl_tax + tax_excl
		order.total_incl_tax = order.total_incl_tax + tax_incl

		order.save()

		print(order)

		self.stdout.write('--Het is gefixt!--')