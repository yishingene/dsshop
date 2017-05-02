from modeltranslation.translator import translator, TranslationOptions
from .models import Product, Category

# translations for products
class ProductTranslationOptions(TranslationOptions):

	fields = ('title', 'description')

translator.register(Product, ProductTranslationOptions)

# translations for categories
class CategoryTranslationOptions(TranslationOptions):

	fields = ('name', 'description')

translator.register(Category, CategoryTranslationOptions)
