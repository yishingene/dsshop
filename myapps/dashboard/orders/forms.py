from django import forms

from oscar.apps.order.models import Order

from decimal import Decimal as D

class ShippingCostForm(forms.ModelForm):

	def clean(self):

		print('----- form clean ')

		cleaned_data = super(ShippingCostForm, self).clean()

		return cleaned_data

		#return super(ShippingCostForm, self).clean()

	def save(self, commit=False):

		print('--------test: %s' % self.instance.total_incl_tax)

		self.instance.total_incl_tax += self.instance.shipping_incl_tax
		self.instance.total_excl_tax += self.instance.shipping_excl_tax

		return super(ShippingCostForm, self).save(commit=True)

	class Meta:
		model = Order
		fields = ['shipping_excl_tax', 'shipping_incl_tax', ]