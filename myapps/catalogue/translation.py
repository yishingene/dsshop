from modeltranslation.translator import translator, TranslationOptions
from .models import Product

class ProductTranslationOptions(TranslationOptions):

	fields = ('title', )


translator.register(Product, ProductTranslationOptions)
