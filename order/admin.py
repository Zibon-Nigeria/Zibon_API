from django.contrib import admin

from order.models import Delivery, Order, OrderItem

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery)