from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import User


# Create your models here.

class ShopperProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shopper_profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.user) + ' shopper profile'
    
    # create shopper profile after user has been created
    @receiver(post_save, sender=User)
    def create_shopper_profile(sender, instance, created, **kwargs):
        if created:
            if instance.account_type == 'Shopper':
                ShopperProfile.objects.create(user=instance)
                instance.shopper_profile.save()


class ShopperPersonalInfo(models.Model):
    id_type = [
        ('passport', "Passport"),
        ('drivers license', "Drivers Licence"),
        ('national id', 'National ID'),
        ('state id', 'State ID')
    ]

    driving_skills = [
        ("None", "I don't know how to drive"),
        ("Learner", "I'm currently learning how to drive"),
        ('Intermediate', 'I have intermediate skills'),
        ( 'Expert',  'I am an expert driver'),
    ]

    shopper = models.OneToOneField(ShopperProfile, on_delete=models.CASCADE, related_name='personalinfo')
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    state_of_origin = models.CharField(max_length=50)
    lga = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)
    criminal_record = models.BooleanField()
    driving_skill = models.CharField(choices=driving_skills, max_length=100, help_text='How would you rate your driving?', blank=True, null=True)
    means_of_id = models.CharField(choices=id_type, max_length=100, help_text='Means of ID?', blank=True, null=True)
    id_document = models.FileField(upload_to='shopper/id_documents/', max_length=100)
    picture = models.FileField(upload_to='shopper/pictures', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{str(self.shopper.user)} info'
    

class BankInfo(models.Model):
    shopper = models.ForeignKey(ShopperProfile, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50)
    account_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.account_name} {self.account_number}'