from django.db import models
from django.template.defaultfilters import slugify
from accounts.models import User
# from products.models import Product

# Create your models here.
class Store(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=50)
    store_address = models.CharField(max_length=200)
    image = models.ImageField(upload_to='stores/', blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.store_name)
    

# category model
class Category(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # overwrite save method
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    
class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_inventory')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=50, blank=True)
    long_description = models.TextField(blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock_qty = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.product_code:
            self.product_code = self._generate_product_code()
        super().save(*args, **kwargs)
        
    def _generate_product_code(self):
        product_code = StoreProduct.objects.order_by('id').last()
        new_id = 1 if not product_code else product_code.id + 1
        return f'prod{new_id:02d}'
        
    def __str__(self):
        return f'{self.name} - {str(self.store)}'
    
    
# product image model
class ProductImage(models.Model):
    product = models.ForeignKey(StoreProduct, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f'{str(self.product.name)} image'
    

# product review model
class Review(models.Model):
    product = models.ForeignKey(StoreProduct, on_delete=models.CASCADE, related_name="product_review")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
    

class Sale(models.Model):
    pass


class SaleItem(models.Model):
    pass