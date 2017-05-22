from django import forms

from oscar.apps.order.models import Order

class ShippingCostForm(forms.ModelForm):

	def clean(self):

		print('----- hIERIEIRZE ')

		return super(ShippingCostForm, self).clean()

	def save(self, commit=False):

		print('----- hIERIEIRZE ')

		return super(ShippingCostForm, self).save(commit=True)

	class Meta:
		model = Order
		fields = ['shipping_excl_tax', 'shipping_incl_tax']