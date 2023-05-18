from django.contrib import admin

from products.models import Category, Product, ProductImage, Review

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Review)