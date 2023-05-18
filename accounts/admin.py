from django.contrib import admin

from accounts.models import CustomUser, ShopperProfile, UserProfile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(ShopperProfile)