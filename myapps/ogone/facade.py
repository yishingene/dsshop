from . import gateway

'''
https://office-server.sips-atos.com/rs-services/v2/checkout/cardOrder
'''

SIPS_HOST = 'https://payment-webinit.simu.sips-atos.com/rs-services/v2/paymentInit/'
SIPS_PATH = '/rs-services/v2/paymentInit/'
SIPS_MERCHANT = '002001000000001'
SIPS_PASSWORD = '002001000000001_KEY1'	# secret key
SIPS_KEY_VERSION = '1'
SIPS_ORDER_CHANNEL = 'INTERNET'
SIPS_INTERFACE_VERSION = 'IR_WS_2.9'
SIPS_CURRENCY_CODE = '978'
SIPS_PAYMENT_MEAN_BRAND = 'BCMC'
SIPS_PAYMENT_MEAN_TYPE = 'CARD'


class Facade(object):
	'''
	De brug tussen Django Oscar en de Payment Gateway van Ogone
	'''

	def __init__(self):
		self.gateway = gateway.Gateway(
			SIPS_HOST, 
			SIPS_MERCHANT,
			SIPS_KEY_VERSION,
			SIPS_ORDER_CHANNEL,
			SIPS_INTERFACE_VERSION,
			SIPS_PAYMENT_MEAN_BRAND,
			SIPS_PAYMENT_MEAN_TYPE
			)

	def handle_response(self, method, order_number, amount, currency, response):

		self.record_txn(method, order_number, amount, currency, response)

		if response.is_successful():
			return response['']

	def record_txn(self, method, order_number, amount, currency, response):

		OrderTransaction.objects.create(
			order_number=order_number,
			method=method,
			amount=amount,
			currency=currency or 'EUR',
			status=response.status,
			)


	def pre_authorise(self, order_number, amount, txn_ref='test', billing_address=None, currency='EUR'):
		'''
		Deze methode roept de gateway aan, en heeft tot doel een voorafbetaling van de gebruiker te verkrijgen
		Hiervoor wordt de pre_auth() methode van de gateway opgeroepen, dewelke een redirection url retouneert
		'''

		try:
			url, redirectionVersion, redirectionData = self.gateway.pre(
			#url = self.gateway.pre(
					amount=amount,
					currency=currency,
					merchantId=SIPS_MERCHANT,
					order_number=order_number
				)

			return url, redirectionVersion, redirectionData
			#return url

		except ValueError:
			print('^^^^ VALUE ERROR ^^^^')

		except:
			print('^^^^ ONBEKENDE ERROR ^^^^')


