from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


from oscar.core.loading import get_classes, get_model
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as OscarProductCreateUpdateView


(
    ProductForm, 

) = get_classes('dashboard.catalogue.forms',(
                    'ProductForm', 
                    )
    )

(
     ProductCategoryFormSet,
     ProductImageFormSet,
     ProductRecommendationFormSet,
     StockRecordFormSet

) = get_classes('dashboard.catalogue.formsets', (
                    'ProductCategoryFormSet',
                    'ProductImageFormSet',
                    'ProductRecommendationFormSet',
                    'StockRecordFormSet'
                    )
    )



Product = get_model('catalogue', 'Product')

def filter_products(queryset, user):
    """
    Restrict the queryset to products the given user has access to.
    A staff user is allowed to access all Products.
    A non-staff user is only allowed access to a product if they are in at
    least one stock record's partner user list.
    """
    if user.is_staff:
        return queryset

    return queryset.filter(stockrecords__partner__users__pk=user.pk).distinct()

class ProductCreateUpdateView(OscarProductCreateUpdateView):
    """
    Dashboard view that is can both create and update products of all kinds.
    It can be used in three different ways, each of them with a unique URL
    pattern:
    - When creating a new standalone product, this view is called with the
      desired product class
    - When editing an existing product, this view is called with the product's
      primary key. If the product is a child product, the template considerably
      reduces the available form fields.
    - When creating a new child product, this view is called with the parent's
      primary key.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/catalogue/product_update.html'
    model = Product
    context_object_name = 'product'

    form_class = ProductForm
    category_formset = ProductCategoryFormSet
    image_formset = ProductImageFormSet
    recommendations_formset = ProductRecommendationFormSet
    stockrecord_formset = StockRecordFormSet

    def __init__(self, *args, **kwargs):
        super(ProductCreateUpdateView, self).__init__(*args, **kwargs)
        self.formsets = {'category_formset': self.category_formset,
                         'image_formset': self.image_formset,
                         'recommended_formset': self.recommendations_formset,
                         'stockrecord_formset': self.stockrecord_formset}

    def dispatch(self, request, *args, **kwargs):
        resp = super(ProductCreateUpdateView, self).dispatch(
            request, *args, **kwargs)
        return self.check_objects_or_redirect() or resp

    def check_objects_or_redirect(self):
        """
        Allows checking the objects fetched by get_object and redirect
        if they don't satisfy our needs.
        Is used to redirect when create a new variant and the specified
        parent product can't actually be turned into a parent product.
        """
        if self.creating and self.parent is not None:
            is_valid, reason = self.parent.can_be_parent(give_reason=True)
            if not is_valid:
                messages.error(self.request, reason)
                return redirect('dashboard:catalogue-product-list')

    def get_queryset(self):
        """
        Filter products that the user doesn't have permission to update
        """
        return filter_products(Product.objects.all(), self.request.user)

    def get_object(self, queryset=None):
        """
        This parts allows generic.UpdateView to handle creating products as
        well. The only distinction between an UpdateView and a CreateView
        is that self.object is None. We emulate this behavior.
        This method is also responsible for setting self.product_class and
        self.parent.
        """
        self.creating = 'pk' not in self.kwargs
        if self.creating:
            # Specifying a parent product is only done when creating a child
            # product.
            parent_pk = self.kwargs.get('parent_pk')
            if parent_pk is None:
                self.parent = None
                # A product class needs to be specified when creating a
                # standalone product.
                product_class_slug = self.kwargs.get('product_class_slug')
                self.product_class = get_object_or_404(
                    ProductClass, slug=product_class_slug)
            else:
                self.parent = get_object_or_404(Product, pk=parent_pk)
                self.product_class = self.parent.product_class

            return None  # success
        else:
            product = super(ProductCreateUpdateView, self).get_object(queryset)
            self.product_class = product.get_product_class()
            self.parent = product.parent
            return product

    def get_context_data(self, **kwargs):
        ctx = super(ProductCreateUpdateView, self).get_context_data(**kwargs)
        ctx['product_class'] = self.product_class
        ctx['parent'] = self.parent
        ctx['title'] = self.get_page_title()

        for ctx_name, formset_class in self.formsets.items():
            if ctx_name not in ctx:
                ctx[ctx_name] = formset_class(self.product_class,
                                              self.request.user,
                                              instance=self.object)
        return ctx

    def get_page_title(self):
        if self.creating:
            if self.parent is None:
                return _('Create new %(product_class)s product') % {
                    'product_class': self.product_class.name}
            else:
                return _('Create new variant of %(parent_product)s') % {
                    'parent_product': self.parent.title}
        else:
            if self.object.title or not self.parent:
                return self.object.title
            else:
                return _('Editing variant of %(parent_product)s') % {
                    'parent_product': self.parent.title}

    def get_form_kwargs(self):
        kwargs = super(ProductCreateUpdateView, self).get_form_kwargs()
        kwargs['product_class'] = self.product_class
        kwargs['parent'] = self.parent
        return kwargs

    def process_all_forms(self, form):
        """
        Short-circuits the regular logic to have one place to have our
        logic to check all forms
        """
        # Need to create the product here because the inline forms need it
        # can't use commit=False because ProductForm does not support it
        if self.creating and form.is_valid():
            self.object = form.save()

        formsets = {}
        for ctx_name, formset_class in self.formsets.items():
            formsets[ctx_name] = formset_class(self.product_class,
                                               self.request.user,
                                               self.request.POST,
                                               self.request.FILES,
                                               instance=self.object)

        is_valid = form.is_valid() and all([formset.is_valid()
                                            for formset in formsets.values()])

        cross_form_validation_result = self.clean(form, formsets)
        if is_valid and cross_form_validation_result:
            return self.forms_valid(form, formsets)
        else:
            return self.forms_invalid(form, formsets)

    # form_valid and form_invalid are called depending on the validation result
    # of just the product form and redisplay the form respectively return a
    # redirect to the success URL. In both cases we need to check our formsets
    # as well, so both methods do the same. process_all_forms then calls
    # forms_valid or forms_invalid respectively, which do the redisplay or
    # redirect.
    form_valid = form_invalid = process_all_forms

    def clean(self, form, formsets):
        """
        Perform any cross-form/formset validation. If there are errors, attach
        errors to a form or a form field so that they are displayed to the user
        and return False. If everything is valid, return True. This method will
        be called regardless of whether the individual forms are valid.
        """
        return True

    def forms_valid(self, form, formsets):
        """
        Save all changes and display a success url.
        When creating the first child product, this method also sets the new
        parent's structure accordingly.
        """
        if self.creating:
            self.handle_adding_child(self.parent)
        else:
            # a just created product was already saved in process_all_forms()
            self.object = form.save()

        # Save formsets
        for formset in formsets.values():
            formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def handle_adding_child(self, parent):
        """
        When creating the first child product, the parent product needs
        to be implicitly converted from a standalone product to a
        parent product.
        """
        # ProductForm eagerly sets the future parent's structure to PARENT to
        # pass validation, but it's not persisted in the database. We ensure
        # it's persisted by calling save()
        if parent is not None:
            parent.structure = Product.PARENT
            parent.save()

    def forms_invalid(self, form, formsets):
        # delete the temporary product again
        if self.creating and self.object and self.object.pk is not None:
            self.object.delete()
            self.object = None

        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"))
        ctx = self.get_context_data(form=form, **formsets)
        return self.render_to_response(ctx)

    def get_url_with_querystring(self, url):
        url_parts = [url]
        if self.request.GET.urlencode():
            url_parts += [self.request.GET.urlencode()]
        return "?".join(url_parts)

    def get_success_url(self):
        """
        Renders a success message and redirects depending on the button:
        - Standard case is pressing "Save"; redirects to the product list
        - When "Save and continue" is pressed, we stay on the same page
        - When "Create (another) child product" is pressed, it redirects
          to a new product creation page
        """
        msg = render_to_string(
            'dashboard/catalogue/messages/product_saved.html',
            {
                'product': self.object,
                'creating': self.creating,
                'request': self.request
            })
        messages.success(self.request, msg, extra_tags="safe noicon")

        action = self.request.POST.get('action')
        if action == 'continue':
            url = reverse(
                'dashboard:catalogue-product', kwargs={"pk": self.object.id})
        elif action == 'create-another-child' and self.parent:
            url = reverse(
                'dashboard:catalogue-product-create-child',
                kwargs={'parent_pk': self.parent.pk})
        elif action == 'create-child':
            url = reverse(
                'dashboard:catalogue-product-create-child',
                kwargs={'parent_pk': self.object.pk})
        else:
            url = reverse('dashboard:catalogue-product-list')
        return self.get_url_with_querystring(url)