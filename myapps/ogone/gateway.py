# -*- coding: utf-8 -*-

import hmac 
import hashlib
import base64
import collections
import json
import requests
import logging
from Crypto.Hash import HMAC, SHA256

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from oscar.apps.payment.exceptions import GatewayError, UnableToTakePayment, PaymentError

#from oscar.apps.payment.exceptions import RedirectRequired, PaymentError, UnableToTakePayment


# SIPS JSON PAYPAGE
SIPS_PAYPAGE_TEST_HOST = 'payment-webinit.simu.sips-atos.com'
SIPS_PAYPAGE_LIVE_HOST = 'payment-webinit.sips-atos.com'
SIPS_PAYPAGE_PATH = '/rs-services/v2/paymentInit/'
SIPS_PAYPAGE_URL = 'https://payment-webinit.simu.sips-atos.com/rs-services/v2/paymentInit/'
SIPS_PAYPAGE_URL_PRODUCTION = 'https://payment-webinit.sips-atos.com/rs-services/v2/paymentInit/'
SIPS_PAYPAGE_SECRET_KEY = '002001000000001_KEY1'
SIPS_PAYPAGE_MERCHANT = '002001000000001'


SIPS_PATH = '/rs-services/v2/paymentInit'
SIPS_MERCHANT = '002001000000001'
SIPS_PASSWORD = '002001000000001_KEY1'	# secret key
SIPS_KEY_VERSION = '1'
SIPS_ORDER_CHANNEL = 'INTERNET'
SIPS_INTERFACE_VERSION = 'IR_WS_2.10'
SIPS_CURRENCY_CODE = '978'
SIPS_PAYMENT_MEAN_BRAND = 'BCMC'
SIPS_PAYMENT_MEAN_TYPE = 'CARD'

# SIPS OFFICE JSON 
SIPS_OFFICE_JSON_HOST = 'office-server.test.sips-atos.com'

SIPS_OFFICE_SECRET_KEY = 'CcDeXSiX2CY0mgbuB_MJxXqXYyJaINZixX2KZgY770o'
SIPS_OFFICE_JSON_MERCHANTID = '037107704346091'
SIPS_OFFICE_JSON_KEYVERSION	= '2'
SIPS_OFFICE_JSON_TEST_CARD_1 = '5017670000000000'
SIPS_EXPIRY_DATE = '201609'
SIPS_OFFICE_INTERFACE_VERSION = 'IR_WS_2.11'


# Response status codes
SUCCESS, MERCHANT_INVALID, TRANSACTION_INVALID, REQUEST_INVALID, SECURITY_ERROR, DUPLICATE_TRANSACTOIN = '00', '03', '12', '30', '34', '94'


logger = logging.getLogger('oscar.checkout')

class SipsPaymentError(PaymentError):
    '''
    Custom subklasse vn Oscar's PaymentError
    '''

    def __init__(self, error_msg):

        self.error_msg = error_msg


def post(url, params):
	'''
	Deze methode voert het post request naar de sips paypage uit, en retourneert het antwoord van de server
	'''

	payload = urlencode(params)

	reponse = requests.post(url, payload, headers={'content-type': 'text/namevalue, charset=utf-8'})


class Gateway(object):

	def __init__(self, sips_url, merchantId='002001000000001', keyVersion='1', orderChannel='INTERNET', interfaceVersion='IR_WS_2.10', paymentMeanBrand='BCMC', paymentMeanType='CARD'):
		
		self._sips_url = sips_url
		self._merchantId = merchantId
		self._keyVersion = keyVersion
		self._orderChannel = orderChannel
		self._interfaceVersion = interfaceVersion
		self._paymentMeanBrand = paymentMeanBrand
		self._paymentMeanType = paymentMeanType


	def _fetch_response(self, **kwargs):
		'''
		execute request
		'''

		print '_fetch_response()'
		print kwargs

		base_url = 'http://127.0.0.1:8000'
		url_path = reverse('sips-place-order')

		#return_url = 'http://127.0.0.1:8000/checkout/thank-you/'
		#return_url = 'http://127.0.0.1:8000/checkout/sips/place-order/' # DEZE WERKTE!!!
		return_url = 'http://127.0.0.1:8000/checkout/preview/' # test 
		return_url = 'http://suikerboon.sites.djangoeurope.com/checkout/preview/' # Host


		basket_amount = int(kwargs['amount'] * 100)

		amount = str(basket_amount)
		automaticResponseUrl = return_url
		currencyCode = '978'
		interfaceVersion = 'IR_WS_2.8'
		keyVersion = '1'
		#merchantId = SIPS_PAYPAGE_MERCHANT	# TEST PAGE
		merchantId = '225005017980001'		# LIVE PAGE
		normalReturnUrl = return_url
		orderChannel = 'INTERNET'
		transactionReference = kwargs['order_number']
		#transactionReference = 'again17'
		#paymentMeanBrandList = ['VISA', 'MASTERCARD']

		request_dict = {
			'amount': amount,
			'automaticResponseUrl': automaticResponseUrl,
			'currencyCode' : currencyCode,
			'interfaceVersion': interfaceVersion,
			'keyVersion' : keyVersion,
			'merchantId': merchantId,
			'normalReturnUrl': normalReturnUrl,
			'orderChannel': orderChannel,
			'transactionReference': transactionReference,
		}

		concat_string = ''

		# SORTEER DE DICTIONARY
		for key in sorted(request_dict):

			concat_string += str(request_dict[key])


		SIPS_PAYPAGE_SECRET_KEY = '8TZkvnUF7pS6LjMNRNp5qzCVk2UKP8R6NHFmyuFPIhk'		# LIVE PAGE
		#SIPS_PAYPAGE_SECRET_KEY = '002001000000001_KEY1'							# TEST PAGE

		# Bereken de secret key voor de huidige gegevens
		signature = self._calculate_seal(concat_string, SIPS_PAYPAGE_SECRET_KEY)

		request_dict['seal'] = signature

		try:
			#response = requests.post(SIPS_PAYPAGE_URL, json=request_dict)				# TEST PAGE
			response = requests.post(SIPS_PAYPAGE_URL_PRODUCTION, json=request_dict)	# LIVE PAGE

		except requests.ConnectionError:

			print 'godver'
			raise SipsPaymentError(mark_safe('Connection Error'))


		json_response = response.json()

		logger.info("sips return code #%s" % json_response['redirectionStatusCode'])


		if json_response['redirectionStatusCode'] == '00':

			print '--------SIPS CONNECTOR: SUCCESS'
			print str(json_response)

			url = str(json_response['redirectionUrl'])
			redirectionVersion = str(json_response['redirectionVersion'])
			redirectionData = str(json_response['redirectionData'])

			print url
			print redirectionVersion
			print redirectionData

			#return url
			return url, redirectionVersion, redirectionData


		else:
			print '--------SIPS CONNECTOR: FAILURE'

			print 'error: ' + str(json_response['redirectionStatusCode'])
			print 'volledige error response: ' + str(json_response)

			if str(json_response['redirectionStatusCode']) == '94':

				raise SipsPaymentError(mark_safe('Er werd reeds een transactie uitgevoerd met deze referentie. ' + \
					'Een duplicaat transactie wordt omwille van veiligheidsredenen niet toegelaten!'))



			else: 

				raise SipsPaymentError(mark_safe('Ander issue'))

			#return 'http://127.0.0.1:8000/checkout/preview/', None, None, json_response['redirectionStatusCode']


		#return response.json()



	def _calculate_seal(self, concat_string, secret_key):
		'''
		Deze methode berekent de HMAC seal
		SHA encryptie seal: http://www.jokecamp.com/blog/examples-of-creating-base64-hashes-using-hmac-sha256-in-different-languages/#python
		'''

		print('*** GATEWAY _calculate_seal()')

		message = bytes(concat_string).encode('utf-8')
		secret = bytes(secret_key) 

		sig = HMAC.new(key=secret, msg=message, digestmod=SHA256).hexdigest()

		return sig


	def _check_kwargs(self, kwargs, required_keys):

		for key in required_keys:

			if not key in kwargs:
				raise ValueError('Je moet %s nog toevoegen als fieds')

		for key in kwargs:

			value = kwargs[key] # de waarde voor een bepaalde key

			if key == 'amount' and value == 0:
				raise ValueError('Een betaling kan niet 0 zijn')


	def pre_auth(self, **kwargs):
		'''
		De pre_auth() methode wordt gebruikt om betaling onmiddellijk te innen. Dit is zowat de gebruikte webshop betaalmethode.

		Het is deze methode die door de Facade wordt opgeroepen
		'''

		print '*** GATEWAY pre() methode'

		return self._fetch_response(**kwargs)

