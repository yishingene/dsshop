from oscar.apps.shipping import repository
from . import methods

class Repository(repository.Repository):
	'''
	Allowed shipping methods
	'''

	methods = (methods.DefferedShippingCost(), methods.SelfService())

