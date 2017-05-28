import datetime

from oscar.apps.order.abstract_models import AbstractOrder

class Order(AbstractOrder):

	def end_date(self):

		end_date = self.date_placed + datetime.timedelta(weeks=4)

		return end_date

from oscar.apps.order.models import *  # noqa

