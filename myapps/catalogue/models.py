from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from oscar.apps.catalogue.abstract_models import AbstractProductImage

from PIL import Image
from io import BytesIO
from imageresize import imageresize

@python_2_unicode_compatible
class ProductImage(AbstractProductImage):
    """
    An image of a product
    """
    original = models.ImageField(_("Original"), upload_to=settings.OSCAR_IMAGE_FOLDER, max_length=255)

    def save(self, *args, **kwargs):

    	pil_image = Image.open(self.original)

    	reduced_image = imageresize.resize_width(pil_image, 1000)

    	#size = 900, 900
    	#pil_image.thumbnail(size, Image.ANTIALIAS)

    	new_image_io = BytesIO()
    	reduced_image.save(new_image_io, format='JPEG')

    	temp_name = self.original.name
    	self.original.delete(save=False) 

    	self.original.save(temp_name, content=ContentFile(new_image_io.getvalue()), save=False)

    	return super(ProductImage, self).save(*args, **kwargs)


from oscar.apps.catalogue.models import *	
