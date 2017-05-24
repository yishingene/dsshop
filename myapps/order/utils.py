from oscar.apps.order.utils import OrderNumberGenerator as OscarOrderNumberGenerator


class OrderNumberGenerator(OscarOrderNumberGenerator):
	'''
	This class is responsible for generating an order number
	'''

	def order_number(self, basket=None):
		'''
		For now: still the default implementation
		'''

		return 100000 + basket.id

