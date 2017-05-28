from django import forms

#from oscar.apps.order.models import Order
from myapps.order.models import Order

from decimal import Decimal as D

class ShippingCostForm(forms.ModelForm):
	'''
	Custom form to allow admin to add shipping charges
	'''

	def clean(self):

		cleaned_data = super(ShippingCostForm, self).clean()

		return cleaned_data

	def save(self, commit=True):

		my_order = super(ShippingCostForm, self).save(commit=True)

		my_order.shipping_incl_tax = self.instance.shipping_excl_tax * D('1.21')

		my_order.total_excl_tax = my_order.basket_total_before_discounts_excl_tax + my_order.shipping_excl_tax
		my_order.total_incl_tax = my_order.basket_total_before_discounts_incl_tax + my_order.shipping_incl_tax

		return super(ShippingCostForm, self).save(commit=True)

	class Meta:
		model = Order
		fields = ['shipping_excl_tax', ]