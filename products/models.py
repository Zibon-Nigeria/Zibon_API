from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.

# category model
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="categories/")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    # overwrite save method
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
# product model
class Product(models.Model):
    category = models.ManyToManyField(Category, related_name="category_product")
    name = models.CharField(max_length=255)
    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="products/")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name
    
# product image model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    product_image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.product.name + ' image'
    
    # def get_absolute_url(self):
    #     return reverse('product_details', kwargs={'id': self.product.id})

# product review model
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_review")
    # user = models.ForeignKey(User, related_name="user")
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.comment

    # def get_absolute_url(self):
    #     return reverse('review', kwargs={'slug': self.id})