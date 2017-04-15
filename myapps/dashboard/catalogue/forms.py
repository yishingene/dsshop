from oscar.apps.dashboard.catalogue.forms import ProductForm as OscarProductForm


class ProductForm(OscarProductForm):

    class Meta(OscarProductForm.Meta):
        fields = [
            'title_nl', 'title_fr', 'title_en', 'upc', 'description', 'is_discountable', 'structure']
