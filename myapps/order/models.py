import datetime

from django.db import models

from oscar.apps.order.abstract_models import AbstractOrder

class Order(AbstractOrder):

	language = models.CharField(blank=True, null=True, max_length=255)
	shipping_confirmed = models.BooleanField(default=False)

	def end_date(self):

		end_date = self.date_placed + datetime.timedelta(weeks=4)
		return end_date

from oscar.apps.order.models import *  # noqa

