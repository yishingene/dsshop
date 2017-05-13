from oscar.core.loading import get_class, get_model
from oscar.apps.dashboard.catalogue.forms import ProductForm as OscarProductForm
from oscar.apps.dashboard.catalogue.forms import ProductImageForm as OscarProductImageForm

from treebeard.forms import movenodeform_factory


Category = get_model('catalogue', 'Category')
ProductImage = get_model('catalogue', 'ProductImage')


class ProductForm(OscarProductForm):
    '''
    This form is used to add the translation fields to the dashboard product edit form
    '''

    class Meta(OscarProductForm.Meta):
        fields = [
            'title_nl',
            'title_fr',
            #'title_en',
            'upc',
            'description',
            'is_discountable',
            'structure'
            ]

# This adds the catagory translations to the dashboard category edit form
CategoryForm = movenodeform_factory(
    Category,
    fields=['name_nl',
    		'name_fr',
    		#'name_en',
    		'description',
    		'image'])

class ProductImageForm(OscarProductImageForm):

    class Meta:
        model = ProductImage
        fields = ['product', 'original', 'caption']
        widgets = {
            'original': ImageInput(),
        }

    def save(self, *args, **kwargs):
        # We infer the display order of the image based on the order of the
        # image fields within the formset.
        kwargs['commit'] = False

        print('we are here!')

        obj = super(ProductImageForm, self).save(*args, **kwargs)
        obj.display_order = self.get_display_order()
        obj.save()
        return obj