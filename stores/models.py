from django.db import models
from accounts.models import User
from products.models import Product

# Create your models here.
class Store(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=50)
    store_address = models.CharField(max_length=200)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.store_name)
    

class StoreInventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_product')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock_qty = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['product', 'store'], name='One store product')
        ]
        
    def __str__(self):
        return f'{str(self.product)} - {str(self.store)}'