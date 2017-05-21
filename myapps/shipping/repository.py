from oscar.apps.shipping import repository
from . import methods

class Repository(repository.Repository):
	'''

	'''

	methods = (methods.DefferedShippingCost(), methods.NoShippingRequired())


# class Repository(repository.Repository):
#     methods = (methods.Free(), methods.NoShippingRequired())