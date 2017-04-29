from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


from oscar.apps.catalogue.abstract_models import AbstractProductImage

from PIL import Image
from io import BytesIO

@python_2_unicode_compatible
class ProductImage(AbstractProductImage):
    """
    An image of a product
    """
    original = models.ImageField(_("Original"), upload_to=settings.OSCAR_IMAGE_FOLDER, max_length=255)

    def save(self, *args, **kwargs):

    	pil_image = Image.open(self.original)

    	size = 1000, 1000
    	pil_image.thumbnail(size, Image.ANTIALIAS)

    	new_image_io = BytesIO()
    	pil_image.save(new_image_io, format='JPEG')

    	temp_name = self.original.name
    	self.original.delete(save=False) 

    	self.original.save(temp_name, content=ContentFile(new_image_io.getvalue()), save=False)

    	return super(ProductImage, self).save(*args, **kwargs)


from oscar.apps.catalogue.models import *	
