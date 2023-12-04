from django.db import models
from accounts.models import User
from stores.models import StoreProduct


# Create your models here.
class Order(models.Model):
    ord_type = [('Pickup', 'Pickup'), ('Delivery', 'Delivery')]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    order_number = models.CharField(max_length=50, blank=True, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    qr_code = models.ImageField(upload_to="orders/qr_codes/", blank=True, null=True)
    order_type = models.CharField(max_length=50, choices=ord_type, default='Delivery')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
        
    def _generate_order_number(self):
        order_number = Order.objects.order_by('id').last()
        new_id = 1 if not order_number else order_number.id + 1
        return f'ord{new_id:02d}'

    def __str__(self):
        return self.order_number
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    order_item = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    has_been_picked_up = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.order_item.retail_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.order_item.name)} - {self.quantity} = {self.subtotal}"
    

class Delivery(models.Model):
    status = [
        ('Available', 'available'),
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]

    shopper = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=50, default="None")
    delivery_status = models.CharField(max_length=50, choices=status, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.order} to {self.delivery_address} - {self.delivery_status}'