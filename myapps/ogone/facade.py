from . import gateway


class Facade(object):
	'''
	De brug tussen Django Oscar en de Payment Gateway van Ogone
	'''

	def __init__(self):
		self.gateway = gateway.Gateway(
			OGONE_PSPID='thinkmobile',
			)


	def pre_authorise(self, order_number, amount, billing_address=None, currency='EUR'):
		'''
		Deze methode roept de gateway aan, en heeft tot doel een voorafbetaling van de gebruiker te verkrijgen
		Hiervoor wordt de pre_auth() methode van de gateway opgeroepen, dewelke een redirection url retouneert
		'''

		try:
			url = self.gateway.pre_auth(
			#url = self.gateway.pre(
					amount=amount,
					currency=currency,
					order_number=order_number
				)

			return url
			#return url

		except ValueError:
			print('^^^^ VALUE ERROR ^^^^')

		except:
			print('^^^^ ONBEKENDE ERROR ^^^^')


