from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse 
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    account_type = (
        ('Customer', 'customer'),
        ('Shopper', 'shopper')
    )

    account_type = models.CharField(_("Account type"), max_length=12, choices=account_type, default='Customer', help_text=_('account type'))
    email = models.EmailField(_("email address"), unique=True)
    fullname = models.CharField(_("full name"), max_length=30)
    phone = models.CharField(_("phone number"), max_length=15, blank=True, null=True)
    address = models.CharField(_("address"), max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='user-image/', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ['firstname', 'lastname', 'address', 'city', 'state']
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    