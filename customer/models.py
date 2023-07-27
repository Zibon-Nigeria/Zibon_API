from django.utils import timezone
from django.db import models
from accounts.models import CustomUser
from stores.models import StoreInventory


# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
        
    def _generate_order_number(self):
        order_number = Order.objects.order_by('id').last()
        new_id = 1 if not order_number else order_number.id + 1
        return f'ORD{new_id:04d}'

    def __str__(self):
        return self.order_number
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(StoreInventory, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.subtotal = self.item.retail_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.item.product)} - {self.quantity} = {self.subtotal}"