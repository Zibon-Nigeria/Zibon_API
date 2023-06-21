from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse 
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    account_options = (
        ('Customer', 'customer'),
        ('Shopper', 'shopper'),
        ('Vendor', 'vendor'),
    )

    account_type = models.CharField(_("Account type"), max_length=12, choices=account_options, default='Customer', help_text=_('account type'))
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ['firstname', 'lastname', 'address', 'city', 'state']
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    # def get_absolute_url(self):
    #     return reverse('profile', kwargs={'username': self.username})


class UserProfile(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    firstname = models.CharField(_("first name"), max_length=30)
    lastname = models.CharField(_("last name"), max_length=30)
    phone = models.CharField(_("phone number"), max_length=15, blank=True, null=True)
    address = models.CharField(_("address"), max_length=255)
    city = models.CharField(_("city"), max_length=30)
    state = models.CharField(_("state"), max_length=30)
    date_cerated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user) + ' customer profile'
    
    # create user profile after user has been created
    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
            instance.userprofile.save()

        
# shopper func
class ShopperProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    

    def __str__(self):
        return str(self.user) + ' shopper profile'
    
    # create shopper profile after user has been created
    @receiver(post_save, sender=CustomUser)
    def create_shopper_profile(sender, instance, created, **kwargs):
        if created:
            if instance.account_type == 'Shopper':
                ShopperProfile.objects.create(user=instance)
                instance.shopperprofile.save()
