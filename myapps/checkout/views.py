
from oscar.core.loading import get_model
from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView

Order = get_model('order', 'Order')

class PaymentDetailsView(OscarPaymentDetailsView):
    '''
    Deze PaymentDetailsView heeft op dit moment geen payment gateway integratie. Het doel is om een basket in
    te dienen, waarbij payment niet wordt geautomatiseerd. 
    '''

    pass 