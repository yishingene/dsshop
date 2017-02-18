import requests
import logging
import hashlib

from django import http
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlencode
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.utils import six

from oscar.core.loading import get_model, get_class

from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from oscar.apps.checkout.views import ThankYouView as OscarThankYouView
from oscar.apps.checkout.session import CheckoutSessionMixin
from oscar.apps.checkout import exceptions
from oscar.apps.checkout import signals
from oscar.apps.payment import models
from oscar.apps.payment.forms import BankcardForm
from oscar.apps.payment.exceptions import RedirectRequired, PaymentError, UnableToTakePayment
from oscar.apps.order.utils import OrderNumberGenerator

from myapps.ogone.facade import Facade
#from myapps.payment.forms import HiddenOgoneForm
#from myapps.ogone.gateway import SipsPaymentError

Order = get_model('order', 'Order')
CheckoutSessionData = get_class('checkout.utils', 'CheckoutSessionData')

logger = logging.getLogger('oscar.checkout')

class PaymentDetailsView(OscarPaymentDetailsView):
    '''
    Deze PaymentDetailsView overschrijft de default django-oscar implementatie, dewelke niets doet.
    Het is verantwoordelijk voor het communiceren met de payment facade en de betaling te initieren.

        * De submit() methode wordt opgeroepen door handle_place_order_submission nadat de gebruiker 
          op de 'Bestelling Plaatsen' knop heeft gedrukt die zich op de preview pagina bevindt
          Deze methode voert dan achtereenvolgens volgende stappen uit: 
            - Een order_number aanmaken
            - De basket gegevens vastleggen zodat deze niet meer gewijzigd kunnen wordne
            - De handle_payment() methode oproepen die de eigenlijke gateway met de service provider initieert
            - Als handle_payment() succesvol was: handle_order_placement() oproepen

        * De handle_payment() methode update django-oscar met de nodige gegevens na betaling. 
          Dit is de methode die je dient te overschrijven. Na afhandeling van de betaling worden de payment sources
          up to date gebracht en en de payment events gelogd
    '''

    def dispatch(self, request, *args, **kwargs):
        # Assign the checkout session manager so it's available in all checkout
        # views.
        self.checkout_session = CheckoutSessionData(request)

        if 'orderID' in request.GET:

            basket = self.get_submitted_basket()

            print('***** basket POST payment: %s' % basket)

            my_submission = self.build_submission_for_basket(basket)

            print('***** submission POST payment: %s' % my_submission)
            

        # Enforce any pre-conditions for the view.
        try:
            self.check_pre_conditions(request)
        except exceptions.FailedPreCondition as e:
            for message in e.messages:
                messages.warning(request, message)
            return http.HttpResponseRedirect(e.url)

        # Check if this view should be skipped
        try:
            self.check_skip_conditions(request)
        except exceptions.PassedSkipCondition as e:
            return http.HttpResponseRedirect(e.url)

        return super(CheckoutSessionMixin, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        print('---- in get() methode van PaymentDetailsView')

        print(request.GET)


        if 'orderID' in request.GET:

            # Als we hier zijn is de betaling succesvol afgehandeld denk ik

            print('------------ hierzo ------------')

            submission = self.build_submission()

            print('***** submission POST payment: %s' % submission)

            payment_kwargs = submission['payment_kwargs']
            basket = submission['basket']
            billing_address = submission['billing_address']
            shipping_charge = submission['shipping_charge']
            shipping_address = submission['shipping_address']
            shipping_method = submission['shipping_method']
            order_total = submission['order_total']
            order_kwargs = submission['order_kwargs']
            user = submission['user']

            order_number = self.generate_order_number(basket)

            # POST PAYMENT: add_payment_event() en add_payment_source
            source_type, __ = models.SourceType.objects.get_or_create(
                        name="Ogone")

            source = models.Source(
                source_type=source_type,
                amount_allocated=basket.total_incl_tax,
                #reference=reference)
                reference=order_number)

            self.add_payment_source(source)

            # Record payment event
            self.add_payment_event('pre-auth', basket.total_incl_tax)

            print('**** Payment source en payment event OK')


            print('going to log now .......')

            signals.post_payment.send_robust(sender=self, view=self)

            # If all is ok with payment, try and place order
            logger.info("Order #%s: payment successful, placing order",
                    order_number)

            # Hier maken we het feitelijke Oscar order aan

            order = self.place_order(order_number=order_number, user=user, basket=basket, shipping_address=shipping_address,
                                        shipping_method=shipping_method, shipping_charge=shipping_charge, 
                                        billing_address=billing_address, order_total=order_total, **order_kwargs)

            print('---- ORDER %s' % order)

            basket.submit()

            return self.handle_successful_order(order)


        else: 
            return super(PaymentDetailsView, self).get(request, *args, **kwargs)

    def build_submission_for_basket(self, basket):
        '''
        CUSTOM METHOD
        '''

        shipping_address = self.get_shipping_address(basket)
        shipping_method = self.get_shipping_method(basket, shipping_address)
        billing_address = self.get_billing_address(shipping_address)
        if not shipping_method: 
            total = shipping_charge = None
        else:
            shipping_charge = shipping_method.calculate(basket)
            total = self.get_order_totals(basket, shipping_charge=shipping_charge)

        submission = {
            'user': self.request.user,
            'basket': basket,
            'shipping_address': shipping_address,
            'shipping_method': shipping_method,
            'shipping_charge': shipping_charge,
            'billing_address': billing_address,
            'order_total': total,
            'order_kwargs': {},
            'payment_kwargs': {}
            }

        if billing_address:
            submission['payment_kwargs']['billing_address'] = billing_address

        if (not user_is_authenticated(submission['user']) and 'guest_email' not in submission['order_kwargs']):
            email = self.checkout_session.get_guest_email()
            submission['order_kwargs']['guest_email'] = email

        return submission


    def handle_payment(self, order_number, total, billing_address, **kwargs):
        '''
        Deze methode is verantwoordelijk voor payment processing 
        ''' 

        print('------ START: checkout view: handle_payment() methode')

        facade = Facade()

        request_dict = facade.pre_authorise(order_number, total.incl_tax, billing_address=billing_address, **kwargs)

        print('!!! succesvol geretourneerd! -- terug in handle_payment() methode')

        #logger.info("Order: redirecting to %s", url)


        # source_type, __ = models.SourceType.objects.get_or_create(
        #             name="Ogone")

        # source = models.Source(
        #     source_type=source_type,
        #     amount_allocated=total.incl_tax,
        #     #reference=reference)
        #     reference=order_number)

        # self.add_payment_source(source)

        # # Record payment event
        # self.add_payment_event('pre-auth', total.incl_tax)


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
            # EDITED: shipping_address toegevoegd aan handle_payment() methode
            self.handle_payment(order_number, order_total, billing_address, **payment_kwargs)

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

        Let op: Deze methode wordt enkel opgeroepen in geval van een POST request (want form submission)
        '''



        # No form data to validate by default, so we simply render the preview
        # page.  If validating form data and it's invalid, then call the
        # render_payment_details view.
        return self.render_preview(request)


    def render_preview(self, request, **kwargs):
        """
        Show a preview of the order.
        If sensitive data was submitted on the payment details page, you will
        need to pass it back to the view here so it can be stored in hidden
        form inputs.  This avoids ever writing the sensitive data to disk.
        """

        # STAP A: Dit is gekopieerde code van de superklasse
        self.preview = True
        ctx = self.get_context_data(**kwargs)

        # STAP B: Haal alle nodige order informatie op (via self.build_submission())
        submission = self.build_submission()

        print('***** submission PRE payment: %s' % submission)

        payment_kwargs = submission['payment_kwargs']
        basket = submission['basket']
        billing_address = submission['billing_address']
        shipping_charge = submission['shipping_charge']
        shipping_address = submission['shipping_address']
        shipping_method = submission['shipping_method']
        order_total = submission['order_total']
        order_kwargs = submission['order_kwargs']
        user = submission['user']

        # STAP C: Maak order nummer aan en freeze basket
        #         Deze code is rechtstreeks gekopieerd van de submit() methode code

        # Taxes must be known at this point
        assert basket.is_tax_known, (
            "Basket tax must be set before a user can place an order")
        assert shipping_charge.is_tax_known, (
            "Shipping charge tax must be set before a user can place an order")

        # We generate the order number first as this will be used
        # in payment requests (ie before the order model has been 
        # created). We also save it in the session for multi-stage
        # checkouts (eg when we redirect to a 3rd party site and place
        # the order on a different request).

        order_number = self.generate_order_number(basket)
        self.checkout_session.set_order_number(order_number)
        logger.info("Order #%s: beginning submission proces for basket #%d" ,
                    order_number, basket.id)

        # Freeze the basket so it cannot be manipulated while the customer is
        # completing payment on a 3rd party site.  Also, store a reference to
        # the basket in the session so that we know which basket to thaw it we
        # get an unsuccessful payment response when redirecting to a 3rd party 
        # site. 

        self.freeze_basket(basket)
        self.checkout_session.set_submitted_basket(basket)

        # We define a general error message for when an unanticipated payment
        # error occurs.
        error_msg = _("A problem occured while processing payment for this "
                      "order - no payment has been taken. Please "
                      "contact customer services if this problem persists")

        signals.pre_payment.send_robust(sender=self, view=self)


        # STAP C: Maak de hidden form fields voor Ogone aan
        
        OGONE_AMOUNT = str(int(order_total.incl_tax * 100))   # Niet-komma getal!
        OGONE_CURRENCY = 'EUR'
        OGONE_LANGUAGE = 'nl_BE'
        OGONE_ORDERID = str(order_number)
        OGONE_PSPID = 'thinkmobile'
        OGONE_SECRET = 'DitIsMijn1stePassPhrase'    # TODO: Dit moet een environ var worden!

        request_dict = {
            'AMOUNT': OGONE_AMOUNT,
            'CURRENCY' : OGONE_CURRENCY,
            'LANGUAGE': OGONE_LANGUAGE,
            'ORDERID': OGONE_ORDERID,
            'PSPID': OGONE_PSPID,
        }

        concat_string = ''

        # SORTEER BOVENSTAANDE DICTIONARY
        for key, value in sorted(request_dict.items()):
            concat_string += str(key) + '=' + str(value) + OGONE_SECRET

        # Bereken de secret key voor de huidige gegevens
        signature = self._calculate_seal(concat_string, OGONE_SECRET)

        request_dict['SHASIGN'] = signature
        
        ctx['OGONE_AMOUNT'] = OGONE_AMOUNT
        ctx['OGONE_PSPID'] = 'thinkmobile'
        ctx['OGONE_LANGUAGE'] = 'nl_BE'
        ctx['OGONE_ORDERID'] = OGONE_ORDERID
        ctx['OGONE_CURRENCY'] = 'EUR'
        ctx['OGONE_SHASIGN'] = signature

        return self.render_to_response(ctx)


    def _calculate_seal(self, concat_string, secret_key):
        '''
        Deze methode berekent de HMAC seal
        SHA encryptie seal: http://www.jokecamp.com/blog/examples-of-creating-base64-hashes-using-hmac-sha256-in-different-languages/#python
        '''
        message = concat_string.encode(encoding='UTF-8')
        secret = secret_key.encode(encoding='UTF-8')

        sig = hashlib.sha256(message).hexdigest()

        return sig


class ThankYouView(OscarThankYouView):
    """
    Displays the 'thank you' page which summarises the order just submitted.
    """
    template_name = 'checkout/thank_you.html'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):

        print('THANKYOUVIEW -- GET() --')

        # logger.info("--TEMM: in get() methode")

        # signals.post_payment.send_robust(sender=self, view=self)

        # # If all is ok with payment, try and place order
        # logger.info("Order #%s: payment successful, placing order",
        #         order_number)

        return super(ThankYouView, self).get(request, *args, **kwargs)


    # def get_object(self):
    #     '''
    #     Opmerking: get_object() is een standaard methode van DetailView (waarvan ThankYouView een subklasse is)
    #     '''

    #     # We allow superusers to force an order thank-you page for testing
    #     #order = None

    #     # if self.request.user.is_superuser:
    #     #     if 'order_number' in self.request.GET:
    #     #         order = Order._default_manager.get(number=self.request.GET['order_number'])

    #     #     elif 'order_id' in self.request.GET:
    #     #         order = Order._default_manager.get(id=self.request.GET['order_id'])

    #     # if not order:
    #     #     if 'checkout_order_id' in self.request.session:
    #     #         order = Order._default_manager.get(pk=self.request.session['checkout_order_id'])

    #     #     elif 'orderID' in self.request.GET:
    #     #         order = Order._default_manager.get(number=self.request.GET['orderID'])

    #     #     else:
    #     #        raise http.Http404(_("No order found"))

    #     return self.order
