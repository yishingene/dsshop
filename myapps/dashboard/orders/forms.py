from django import forms

from oscar.apps.order.models import Order

from decimal import Decimal as D

class ShippingCostForm(forms.ModelForm):
	'''
	Custom form to allow admin to add shipping charges
	'''

	def clean(self):

		cleaned_data = super(ShippingCostForm, self).clean()

		return cleaned_data

	def save(self, commit=False):

		total_incl_tax = self.instance.basket_total_before_discounts_incl_tax
		total_excl_tax = self.instance.basket_total_before_discounts_excl_tax

		self.instance.total_incl_tax = self.instance.shipping_incl_tax + total_incl_tax
		self.instance.total_excl_tax = self.instance.shipping_excl_tax + total_excl_tax

		return super(ShippingCostForm, self).save(commit=True)

	class Meta:
		model = Order
		fields = ['shipping_excl_tax', 'shipping_incl_tax', ]