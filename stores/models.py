from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import CustomUser
from products.models import Product

# Create your models here.

class Store(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='store_owner')
    balance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return str(self.owner) + ' store'
    

    # create shopper profile after user has been created
    @receiver(post_save, sender=CustomUser)
    def create_shopper_profile(sender, instance, created, **kwargs):
        if created:
            if instance.account_type == 'Vendor':
                Store.objects.create(user=instance)
    
    # save shopper profile
    @receiver(post_save, sender=CustomUser)
    def save_shopper_profile(sender, instance, **kwargs):
        if instance.account_type == 'Vendor':
            instance.store.save()


class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_product')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock_qty = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'store'], name='follow once')
        ]
    
    def __str__(self):
        return self.product