from django.contrib import admin

from stores.models import Store, StoreInventory

# Register your models here.
admin.site.register(Store)
admin.site.register(StoreInventory)
