from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from accounts.models import CustomUser
from customer.models import Order
import shopper

# Create your models here.

class ShopperProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='shopper_profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user) + ' shopper profile'
    
    # create shopper profile after user has been created
    @receiver(post_save, sender=CustomUser)
    def create_shopper_profile(sender, instance, created, **kwargs):
        if created:
            if instance.account_type == 'Shopper':
                ShopperProfile.objects.create(user=instance)
                instance.shopperprofile.save()


class Delivery(models.Model):
    delivery_status = [
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]

    shopper = models.ForeignKey(ShopperProfile, on_delete=models.CASCADE, related_name='deliveries')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    destination = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=delivery_status)
    date_created = models.DateTimeField(default=timezone.now)


class ShopperPersonalInfo(models.Model):
    shopper = models.OneToOneField(ShopperProfile, on_delete=models.CASCADE, related_name='personalinfo')
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    state_of_origin = models.CharField(max_length=50)
    lga = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    criminal_record = models.BooleanField()
    id_document = models.FileField(upload_to='shopper/id_documents/', max_length=100)
    picture = models.FileField(upload_to='shopper/pictures', max_length=100)

    def __str__(self):
        return f'{str(self.shopper.user)} info'
    

class BankInfo(models.Model):
    shopper = models.ForeignKey(ShopperProfile, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50)
    account_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.account_name} {self.account_number}'