from oscar.core.loading import get_class, get_model
from oscar.apps.dashboard.catalogue.forms import ProductForm as OscarProductForm

from treebeard.forms import movenodeform_factory


Category = get_model('catalogue', 'Category')


class ProductForm(OscarProductForm):

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


CategoryForm = movenodeform_factory(
    Category,
    fields=['name_nl',
    		'name_fr',
    		#'name_en',
    		'description',
    		'image'])