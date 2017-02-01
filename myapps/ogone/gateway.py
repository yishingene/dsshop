# -*- coding: utf-8 -*-

import hmac 
import hashlib
import base64
import json
import requests
import logging
#from Crypto.Hash import HMAC, SHA256

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from oscar.apps.payment.exceptions import GatewayError, UnableToTakePayment, PaymentError

#from oscar.apps.payment.exceptions import RedirectRequired, PaymentError, UnableToTakePayment

# VERPLICHTE VELDEN: PSPID, ORDERID, AMOUNT, CURRENCY en LANGUAGE

OGONE_PSPID = 'thinkmobile'
OGONE_CURRENCY = 'EUR'
OGONE_LANGUAGE = 'nl_BE'
OGONE_SECRET = 'DitIsMijn1stePassPhrase'

OGONE_TEST_URL = 'https://secure.ogone.com/ncol/test/orderstandard.asp'

logger = logging.getLogger('oscar.checkout')


def post(url, params):
	'''
	Deze methode voert het post request naar de sips paypage uit, en retourneert het antwoord van de server.
	Hier wordt het vereiste web form voor Ogone dus verstuurd
	'''

	payload = urlencode(params)

	reponse = requests.post(url, payload, headers={'content-type': 'text/namevalue, charset=utf-8'})


class Gateway(object):

	def __init__(self, OGONE_PSPID):
		
		self._PSPID = OGONE_PSPID

	def pre_auth(self, **kwargs):
		'''
		De pre_auth() methode wordt gebruikt om betaling onmiddellijk te innen. Dit is zowat de gebruikte webshop betaalmethode.
		Het is deze methode die door de Facade wordt opgeroepen
		'''

		print('*** GATEWAY pre() methode')

		return self._fetch_response(**kwargs)

	def _fetch_response(self, **kwargs):
		'''
		execute request
		'''

		print('_fetch_response()')
		print('GATEWAY KWARGS: %s' % kwargs)

		basket_amount = int(kwargs['amount'] * 100)
		amount = str(basket_amount)

		order_id_nr = kwargs['order_number']
		order_id = str(order_id_nr)

		request_dict = {
			'AMOUNT': amount,
			'CURRENCY' : OGONE_CURRENCY,
			'LANGUAGE': OGONE_LANGUAGE,
			'ORDERID': order_id,
			'PSPID': OGONE_PSPID,
		}

		print('^^^REQUEST DICT :%s' % request_dict)

		concat_string = ''

		# SORTEER DE DICTIONARY
		for key in sorted(request_dict):
			concat_string += str(request_dict[key]) + OGONE_SECRET

		print('^^^CONCAT string :%s' % concat_string)

		# Bereken de secret key voor de huidige gegevens
		signature = self._calculate_seal(concat_string, OGONE_SECRET)

		request_dict['SHASIGN'] = signature

		print('^^^SIGNATURE: %s' % signature)

		try:
			response = requests.post(SIPS_PAYPAGE_URL_PRODUCTION, json=request_dict)	# LIVE PAGE

		except requests.ConnectionError:

			print('godver')
			raise SipsPaymentError(mark_safe('Connection Error'))


		json_response = response.json()

		logger.info("sips return code #%s" % json_response['redirectionStatusCode'])


		if json_response['redirectionStatusCode'] == '00':

			print('--------SIPS CONNECTOR: SUCCESS')
			print(str(json_response))

			url = str(json_response['redirectionUrl'])
			redirectionVersion = str(json_response['redirectionVersion'])
			redirectionData = str(json_response['redirectionData'])

			print(url)
			print(redirectionVersion)
			print(redirectionData)

			return url
			#return url, redirectionVersion, redirectionData


		else:
			print('--------SIPS CONNECTOR: FAILURE')

			print('error: ' + str(json_response['redirectionStatusCode']))
			print('volledige error response: ' + str(json_response))

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
		print('alles oke tot hier? 0')

		message = concat_string.encode('utf-8')
		print('alles oke tot hier? 1')

		secret = secret_key.encode('utf-8')
		print('alles oke tot hier?2')

		sig = HMAC.new(key=secret, msg=message, digestmod=SHA256).hexdigest()

		print('sig berekend?')

		return sig


