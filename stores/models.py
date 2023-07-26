from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import CustomUser
from products.models import Product

# Create your models here.

class Store(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=50, blank=True, null=True)
    store_address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        
        return str(self.store_name) if self.store_name else str(self.owner) + ' store'
    

    # create shopper profile after user has been created
    @receiver(post_save, sender=CustomUser)
    def create_shopper_profile(sender, instance, created, **kwargs):
        if created:
            if instance.account_type == 'Vendor':
                Store.objects.create(owner=instance)
                instance.store.save()


class StoreInventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_product')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock_qty = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'store'], name='follow once')
        ]
        
    def __str__(self):
        return str(self.product) + " from " + str(self.store)