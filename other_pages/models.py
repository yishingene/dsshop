import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField


# Create your models here.

class Event(models.Model):

	name = models.CharField(_('naam'), max_length=64)
	date = models.DateField('startdatum', default=datetime.date.today)
	duration = models.PositiveIntegerField('aantal dagen', default=1)
	website = models.URLField(_('website link'), blank=True)
	location = models.CharField(_('locatie (stad)'), max_length=64)
	country = CountryField('location (land)', default='BE')

	class Meta:
		verbose_name = 'beurs'
		verbose_name_plural = 'beurzen'
		ordering = ['-date', ]

	def __str__(self):

		return self.name + ' - ' + self.location

	def end_date(self):

		difference = self.duration - 1
		return self.date + datetime.timedelta(days=difference)

