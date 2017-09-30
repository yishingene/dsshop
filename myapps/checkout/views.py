from decimal import Decimal as D

from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.template.loader import get_template

from oscar.core.loading import get_model
from oscar.apps.checkout import exceptions
from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView

Order = get_model('order', 'Order')



class PaymentDetailsView(OscarPaymentDetailsView):
	'''
	Deze PaymentDetailsView heeft op dit moment geen payment gateway integratie. Het doel is om een basket in
	te dienen, waarbij payment niet wordt geautomatiseerd. 
	'''

	skip_conditions = ['skip_unless_payment_is_required']

	def submit(self, user, basket, shipping_address, shipping_method,
			shipping_charge, billing_address, order_total, payment_kwargs=None, order_kwargs=None):

		self.send_mail(user, basket, order_total)

		return super(PaymentDetailsView, self).submit(user=user, basket=basket, shipping_address=shipping_address,
			shipping_method=shipping_method, shipping_charge=shipping_charge, billing_address=billing_address,
			order_total=order_total, payment_kwargs=payment_kwargs, order_kwargs=order_kwargs)

	def send_mail(self, user, basket, order_total):

		subject = 'Nieuwe bestelling op website!' + ' > van: ' + user.email
		receivers = ['info@tomverheyden.com', 'tim.claes@live.be']
		sender = 'info@tomverheyden.com'

		ctx = {}

		ctx['basket'] = basket
		ctx['order_total'] = order_total
		ctx['user'] = user

		message = get_template('checkout/email/new_order.html').render(ctx)
		msg = EmailMessage(subject, message, to=receivers, from_email=sender)
		msg.content_subtype = 'html'
		msg.send()

	def skip_unless_payment_is_required(self, request):
		# Check to see if payment is actually required for this order.
		shipping_address = self.get_shipping_address(request.basket)
		shipping_method = self.get_shipping_method(request.basket, shipping_address)

		if shipping_method:
			shipping_charge = shipping_method.calculate(request.basket)

			# Als klant komt afhalen: betaling info niet nodig!
			if shipping_method.code == 'Afhaling door klant':
				raise exceptions.PassedSkipCondition(url=reverse('checkout:preview'))

		else:
			# It's unusual to get here as a shipping method should be set by
			# the time this skip-condition is called. In the absence of any
			# other evidence, we assume the shipping charge is zero.
			shipping_charge = prices.Price(
								currency=request.basket.currency, excl_tax=D('0.00'),
								tax=D('0.00')
								)

		total = self.get_order_totals(request.basket, shipping_charge)

		if total.excl_tax == D('0.00'):
			raise exceptions.PassedSkipCondition(
				url=reverse('checkout:preview')
				)


	def get_skip_conditions(self, request):
		if not self.preview:
			# Payment details should only be collected if necessary
			return ['skip_unless_payment_is_required']

		return super(PaymentDetailsView, self).get_skip_conditions(request)


	def check_skip_conditions(self, request):

		# self.preview check is nodig, anders infinite redirects!
		if not self.preview:
			skip_conditions = self.get_skip_conditions(request)

			for method_name in skip_conditions:
				if not hasattr(self, method_name):
					raise ImproperlyConfigured(
						"There is no method '%s' to call as a skip-condition" % (
						method_name))

				getattr(self, method_name)(request)
