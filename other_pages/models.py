from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class Event(models.Model):

	name = models.CharField(_('naam'), max_length=64)
	date = models.DateField(_('datum'))
	website = models.URLField(_('website link'), blank=True)
	location = models.CharField(_('locatie (stad)'), max_length=64)

	class Meta:
		verbose_name = 'beurs'
		verbose_name_plural = 'beurzen'
		ordering = ['-date', ]

	def __str__(self):

		return self.name + ' - ' + self.location