from django.contrib import admin

from stores.models import Inventory, Store

# Register your models here.
admin.site.register(Store)
admin.site.register(Inventory)
