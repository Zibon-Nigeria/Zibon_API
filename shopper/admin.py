from django.contrib import admin

from shopper.models import BankInfo, ShopperPersonalInfo, ShopperProfile

# Register your models here.
admin.site.register(ShopperProfile)
admin.site.register(BankInfo)
admin.site.register(ShopperPersonalInfo)