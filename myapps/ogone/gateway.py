# -*- coding: utf-8 -*-

import hmac 
import hashlib
import base64
import json
import requests
import logging
import collections
from Crypto.Hash import HMAC, SHA256, SHA
from Crypto.Util import py3compat

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from oscar.apps.payment.exceptions import GatewayError, UnableToTakePayment, PaymentError, RedirectRequired

#from oscar.apps.payment.exceptions import RedirectRequired, PaymentError, UnableToTakePayment

# VERPLICHTE VELDEN: PSPID, ORDERID, AMOUNT, CURRENCY en LANGUAGE

OGONE_PSPID = 'thinkmobile'
OGONE_CURRENCY = 'EUR'
OGONE_LANGUAGE = 'nl_BE'
#OGONE_SECRET = 'DitIsMijn1stePassPhrase'
OGONE_SECRET = 'DitIsMijn2dePassphrase!'


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

		concat_string = ''

		# SORTEER DE DICTIONARY
		for key, value in sorted(request_dict.items()):
			concat_string += str(key) + '=' + str(value) + OGONE_SECRET

		print('^^^CONCAT string :%s' % concat_string)

		# Bereken de secret key voor de huidige gegevens
		signature = self._calculate_seal(concat_string, OGONE_SECRET)

		request_dict['SHASIGN'] = signature

		return request_dict


		print('ogone response: %s' % response)
		print(response.text)



	def _calculate_seal(self, concat_string, secret_key):
		'''
		Deze methode berekent de HMAC seal
		SHA encryptie seal: http://www.jokecamp.com/blog/examples-of-creating-base64-hashes-using-hmac-sha256-in-different-languages/#python
		'''
		message = concat_string.encode(encoding='UTF-8')
		secret = secret_key.encode(encoding='UTF-8')

		#sig = hashlib.sha1(message).hexdigest() # Also possible and tested!
		sig = hashlib.sha256(message).hexdigest()

		#print('signature: %s' % sig)

		return sig
