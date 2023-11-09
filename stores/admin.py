from django.contrib import admin

from stores.models import Category, ProductImage, Review, Sale, SaleItem, Store, StoreProduct

# Register your models here.
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(StoreProduct)
admin.site.register(Review)
admin.site.register(Sale)
admin.site.register(SaleItem)


