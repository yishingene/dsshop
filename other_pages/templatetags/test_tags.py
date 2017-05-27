from django import template

from myapps.order.models import Order

register = template.Library()

@register.simple_tag
def get_payment_event(order):

	return order.payment_events.all()

