import requests
import logging

from django import http
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlencode
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.utils import six

from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from oscar.apps.checkout.views import OrderPlacementMixin
from oscar.apps.checkout.views import ThankYouView as OscarThankYouView
from oscar.apps.checkout import signals
from oscar.apps.payment import models
from oscar.apps.payment.forms import BankcardForm
from oscar.apps.payment.exceptions import RedirectRequired, PaymentError, UnableToTakePayment
from oscar.apps.order.utils import OrderNumberGenerator

#from myapps.ogone.facade import Facade
#from myapps.ogone.gateway import SipsPaymentError


logger = logging.getLogger('oscar.checkout')

class OgoneRedirectRequired(RedirectRequired):
    '''
    Custom subklasse van Oscar's RedirectRequired, voegt geen functionaliteit toe!
    '''

    def __init__(self, url):
        self.url = url


class PaymentDetailsView(OscarPaymentDetailsView):
    '''
    Deze PaymentDetailsView overschrijft de default django-oscar implementatie, dewelke niets doet.
    Het is verantwoordelijk voor het communiceren met de payment facade en de betaling te initieren.
    De submit() methode 
    De handle_payment() methode update django-oscar met de nodige gegevens na betaling
    '''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentDetailsView, self).dispatch(request, *args, **kwargs)


    def handle_payment(self, order_number, total, **kwargs):
        '''
        Deze methode is verantwoordelijk voor payment processing 
        ''' 

        print('!!! START: checkout view: handle_payment() methode')

        facade = Facade()

        reference = facade.pre_authorise(order_number, total.incl_tax, **kwargs)

        print('!!! succesvol geretourneerd! -- terug in handle_payment() methode')

        #logger.info("Order: redirecting to %s", url)

        
        source_type, __ = models.SourceType.objects.get_or_create(
                    name="Ogone")

        source = models.Source(
            source_type=source_type,
            amount_allocated=total.incl_tax,
            #reference=reference)
            reference=order_number)

        self.add_payment_source(source)

        # Record payment event
        self.add_payment_event('pre-auth', total.incl_tax)


    def submit(self, user, basket, shipping_address, shipping_method,  # noqa (too complex (10))
            shipping_charge, billing_address, order_total,
            payment_kwargs=None, order_kwargs=None):
        """
        Submit a basket for order placement.
        The process runs as follows:
            * Generate an order number
            * Freeze the basket so it cannot be modified any more (important when
                redirecting the user to another site for payment as it prevents the
                basket being manipulated during the payment process).
            * Attempt to take payment for the order
                - If payment is successful, place the order
                - If a redirect is required (eg PayPal, 3DSecure), redirect
                - If payment is unsuccessful, show an appropriate error message
        
        :basket: The basket to submit.
        :payment_kwargs: Additional kwargs to pass to the handle_payment
                method. It normally makes sense to pass form
                instances (rather than model instances) so that the
                forms can be re-rendered correctly if payment fails.
        :order_kwargs: Additional kwargs to pass to the place_order method
        """
        if payment_kwargs is None:
            payment_kwargs = {}
        if order_kwargs is None:
            order_kwargs = {}

        # Taxes must be known at this point
        assert basket.is_tax_known, (
            "Basket tax must be set before a user can place an order")
        assert shipping_charge.is_tax_known, (
            "Shipping charge tax must be set before a user can place an order")

        # We generate the order number first as this will be used
        # in payment requests (ie before the order model has been
        # created).  We also save it in the session for multi-stage
        # checkouts (eg where we redirect to a 3rd party site and place
        # the order on a different request).
        order_number = self.generate_order_number(basket)
        self.checkout_session.set_order_number(order_number)
        logger.info("Order #%s: beginning submission process for basket #%d",
                order_number, basket.id)

        # Freeze the basket so it cannot be manipulated while the customer is
        # completing payment on a 3rd party site.  Also, store a reference to
        # the basket in the session so that we know which basket to thaw if we
        # get an unsuccessful payment response when redirecting to a 3rd party
        # site.
        self.freeze_basket(basket)
        self.checkout_session.set_submitted_basket(basket)

        # We define a general error message for when an unanticipated payment
        # error occurs.
        error_msg = _("A problem occurred while processing payment for this "
            "order - no payment has been taken.  Please "
            "contact customer services if this problem persists")

        signals.pre_payment.send_robust(sender=self, view=self)

        try:
            self.handle_payment(order_number, order_total, **payment_kwargs)

        # except SipsRedirectRequired as e:

        #     print('SipsRedirectRequired!')

        #     logger.info("Order #%s: redirecting to %s", order_number, e.url)

        #     data = {
        #         'redirectionVersion': e.redirectionVersion,
        #         'redirectionData': e.redirectionData
        #     }

        #     # urlencode retourneert url parameters
        #     payload = urlencode(data)

        #     # volledige url bestaat uit base url + urlencoded parameters
        #     complete_url = '%s?%s' % (e.url, payload)

        #     return http.HttpResponseRedirect(complete_url)

        except RedirectRequired as e:
            # Redirect required (eg PayPal, 3DS)
            logger.info("Order #%s: redirecting to %s", order_number, e.url)
            return http.HttpResponseRedirect(e.url)

        except UnableToTakePayment as e:
            # Something went wrong with payment but in an anticipated way.  Eg
            # their bankcard has expired, wrong card number - that kind of
            # thing. This type of exception is supposed to set a friendly error
            # message that makes sense to the customer.
            msg = six.text_type(e)
            logger.warning(
                    "Order #%s: unable to take payment (%s) - restoring basket",
                    order_number, msg)
            self.restore_frozen_basket()

            # We assume that the details submitted on the payment details view
            # were invalid (eg expired bankcard).
            return self.render_payment_details(
                    self.request, error=msg, **payment_kwargs)

        except SipsPaymentError as e:

            msg = six.text_type(e)
            logger.error("Order #%s: payment error (%s)", order_number, msg,
                    exc_info=True)
            self.restore_frozen_basket()

            return self.render_preview(
                    self.request, error=e.error_msg, **payment_kwargs)

        except PaymentError as e:
            # A general payment error - Something went wrong which wasn't
            # anticipated.  Eg, the payment gateway is down (it happens), your
            # credentials are wrong - that king of thing.
            # It makes sense to configure the checkout logger to
            # mail admins on an error as this issue warrants some further
            # investigation.
            msg = six.text_type(e)
            logger.error("Order #%s: payment error (%s)", order_number, msg,
                    exc_info=True)
            self.restore_frozen_basket()

            return self.render_preview(
                    self.request, error=error_msg, **payment_kwargs)

        except Exception as e:
            # Unhandled exception - hopefully, you will only ever see this in
            # development...
            logger.error(
                    "Order #%s: unhandled exception while taking payment (%s)",
                    order_number, e, exc_info=True)
            self.restore_frozen_basket()

            return self.render_preview(
                    self.request, error=error_msg, **payment_kwargs)

        print('going to log now .......')

        signals.post_payment.send_robust(sender=self, view=self)

        # If all is ok with payment, try and place order
        logger.info("Order #%s: payment successful, placing order",
                order_number)

        try:
            return self.handle_order_placement(
                    order_number, user, basket, shipping_address, shipping_method,
                    shipping_charge, billing_address, order_total, **order_kwargs)

        except UnableToPlaceOrder as e:
            # It's possible that something will go wrong while trying to
            # actually place an order.  Not a good situation to be in as a
            # payment transaction may already have taken place, but needs
            # to be handled gracefully.
            msg = six.text_type(e)
            logger.error("Order #%s: unable to place order - %s",
                    order_number, msg, exc_info=True)
            self.restore_frozen_basket()

            return self.render_preview(
                    self.request, error=msg, **payment_kwargs)


    def handle_payment_details_submission(self, request):
        '''
        Deze methode wordt opgeroepen wanneer je in de checkout procedure naar de 'preview' stap gaat
        Hij is vereist wanneer de gebruiker een bijkomend form (vb bankkaart formulier) dient in te vullen
        De methode leidt de gebruiker verder naar het preview view wanneer de submitted data correct is
        Wanneer de data incorrect is wordt het view opnieuw gerenderd met de nodige foutmeldingen
        '''

        '''
        In dit geval is het form dat we nodig hebben het BankcardForm uit de payment app
        '''

        # No form data to validate by default, so we simply render the preview
        # page.  If validating form data and it's invalid, then call the
        # render_payment_details view.
        return self.render_preview(request)




