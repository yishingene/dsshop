from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template


from oscar.core.loading import get_model
from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView

Order = get_model('order', 'Order')

class PaymentDetailsView(OscarPaymentDetailsView):
	'''
	Deze PaymentDetailsView heeft op dit moment geen payment gateway integratie. Het doel is om een basket in
	te dienen, waarbij payment niet wordt geautomatiseerd. 
	'''

	def submit(self, user, basket, shipping_address, shipping_method,
			shipping_charge, billing_address, order_total, payment_kwargs=None, order_kwargs=None):

		self.send_mail(user.email)


		return super(PaymentDetailsView, self).submit(user=user, basket=basket, shipping_address=shipping_address,
			shipping_method=shipping_method, shipping_charge=shipping_charge, billing_address=billing_address,
			order_total=order_total, payment_kwargs=payment_kwargs, order_kwargs=order_kwargs)

	def send_mail(self, user_email):

		subject = 'Nieuwe bestelling op website!' + ' van: ' + user_email
		receivers = ['info@tomverheyden.com', 'tim.claes@live.be', ]
		sender = 'website@tomverheyden.com'

		ctx = {}

		message = get_template('checkout/email/new_order.html').render(Context(ctx))
		msg = EmailMessage(subject, message, to=receivers, from_email=sender)
		msg.content_subtype = 'html'
		msg.send()
