from typing import Required
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from decimal import Decimal

class Category(models.Model):
    DEVICE_CHOICES = [
        ("Mobile", "Mobile"),
        ("Tablet", "Tablet"),
        ("Laptop",'Laptop'),
        ("Watch","Watch"),
        ("Gadget","Gadget"),
        ("Speaker","Speaker"),
        ("Accessories","Accessories"),
        ("Computer","Computer"),
    ]
    name = models.CharField(max_length=255, choices=DEVICE_CHOICES)
    
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="main_category")
    def __str__(self):
        return self.name


# class Product(models.Model):
#     name = models.CharField(max_length=255) 
#     sku = models.CharField(max_length=100, unique=True)  
#     category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
#     warranty = models.CharField(max_length=255)  
#     availability = models.CharField(max_length=100) 
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
#     discount = models.PositiveIntegerField(null=True, blank=True)  
#     features = models.TextField()
#     # Support both image file and URL for backward compatibility
#     image = models.ImageField(upload_to='products/', null=True, blank=True, help_text="Upload product image")
#     image_url = models.URLField(max_length=500, null=True, blank=True, help_text="Or provide image URL (if not uploading file)")

#     def __str__(self):
#         return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    # sku = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    warranty = models.CharField(max_length=255)
    availability = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)

    features = models.TextField()

    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url or ''

    @property
    def image_display_url(self):
        """Property for template compatibility"""
        return self.get_image_url()
    
    @property
    def calculated_discount_percent(self):
        if self.original_price and self.price and self.original_price > self.price:
            return round(
                ((self.original_price - self.price) / self.original_price) * 100,
                2
            )
        return 0

    @property
    def final_price(self):
        return self.price

    def __str__(self):
        return self.name

    
class Features(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    
    def __str__(self):
        return self.name    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    # Support both image file and URL for backward compatibility
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    # image = models.ImageField(upload_to='products/gallery/', null=True, blank=True, help_text="Upload product image")
    image_url = models.URLField(max_length=500, null=True, blank=True, help_text="Or provide image URL (if not uploading file)")

    def __str__(self):
        return f"Image for {self.product.name}"
    
    def get_image_url(self):
        """Return image URL - prefer uploaded image over URL field"""
        if self.image:
            return self.image.url
        return self.image_url or ''

class cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pro_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.ForeignKey(ProductImage, on_delete=models.CASCADE , null=True , blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total = models.IntegerField(default=0)
    grand_total = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.pro_id.name}, {self.quantity}"

    

class Address(models.Model):
    first_name = models.CharField(max_length=255 , null=True , blank=True)
    last_name = models.CharField(max_length=255 , null=True , blank=True )
    address = models.CharField(max_length=255)
    area_code = models.IntegerField()
    phone_number = models.IntegerField()
    zip_code = models.IntegerField()
    company = models.CharField(max_length=25 , null=True , blank=True)
    business = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='addresses')
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Dynamic Content Models
class Slider(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sliders')
    title = models.CharField(max_length=255)
    description = models.TextField()
    background_image_url = models.URLField(max_length=500)
    product_image_url = models.URLField(max_length=500, null=True, blank=True)
    position = models.CharField(max_length=20, choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')], default='center')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Promotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='promotions', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price_text = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.URLField(max_length=500)
    background_color = models.CharField(max_length=50, default='bg-silver', help_text="CSS class for background color")
    link_url = models.URLField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=20, choices=[('lg', 'Large'), ('sm', 'Small')], default='sm')
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}/5)"

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo_url = models.URLField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class SiteSettings(models.Model):
    facebook_url = models.URLField(max_length=500, null=True, blank=True)
    twitter_url = models.URLField(max_length=500, null=True, blank=True)
    instagram_url = models.URLField(max_length=500, null=True, blank=True)
    google_plus_url = models.URLField(max_length=500, null=True, blank=True)
    dribbble_url = models.URLField(max_length=500, null=True, blank=True)
    newsletter_email = models.EmailField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class FooterLink(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title