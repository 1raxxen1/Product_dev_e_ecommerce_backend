from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector
# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    search_vector = SearchVectorField(null=True)

    class Meta: indexes = [ 
        GinIndex(fields=['search_vector']),
        models.Index(fields=['slug']),
        models.Index(fields=['category']),
        models.Index(fields=['is_active']),
     ]


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['product']),
            models.Index(fields=['is_active']),
        ]


    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
class Inventory(models.Model):
    variant = models.OneToOneField(Variant, on_delete=models.CASCADE, related_name='inventory')
    stock = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.variant.sku} | Stock: {self.stock}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(("Image"), upload_to='product_images/', height_field=None, width_field=None, max_length=None)
    alt_text = models.CharField(max_length=255, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.product.name} Image {self.order}"
    
#Amazon types of products

class ProductContentBlock(models.Model):
    BLOCK_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('spec', 'specification'),

    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='content_blocks')

    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(("image"), upload_to='product_content_blocks/', height_field=None, width_field=None, max_length=None)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.product.name} Content Block {self.order}"
    
@receiver(post_save, sender=Product)
def update_search_vector(sender, instance, **kwargs):
    Product.objects.filter(id=instance.id).update(
        search_vector=(
            SearchVector('name', weight='A') +
            SearchVector('description', weight='B')
        )
    )

