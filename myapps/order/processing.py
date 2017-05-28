from oscar.apps.order.processing import EventHandler as OscarEventHandler
from myapps.order.models import PaymentEvent, PaymentEventType
from oscar.apps.payment import models as paymentmodels
from oscar.apps.checkout import signals
from myapps.checkout.views import PaymentDetailsView

class EventHandler(OscarEventHandler):

	def handle_order_status_change(self, order, new_status, note_msg=None):

		if new_status == 'Betaald':

			print('Tis betaald!')

			view = PaymentDetailsView()

			source_type, __ = paymentmodels.SourceType.objects.get_or_create(name="Overschrijving")

			source = paymentmodels.Source(
				source_type=source_type,
				amount_allocated=order.total_incl_tax,
				reference=order.number,
				order=order,
				)
			source.save()

			payment_event_type, created = PaymentEventType.objects.get_or_create(name='Betaald')
			payment_event_type.save()

			payment_event = PaymentEvent(order=order, event_type=payment_event_type, amount=order.total_incl_tax, reference=order.number)
			payment_event.save()

			signals.post_payment.send_robust(sender=view, view=view)

		order.set_status(new_status)

		if note_msg:
			self.create_note(order, note_msg)