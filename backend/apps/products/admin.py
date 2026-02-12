from django.contrib import admin

from .models import Product, ProductCategory, ProductImage, Variant

# Register your models here.
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'updated_at', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_url', 'alt_text', 'order')
    list_filter = ('product',)
    search_fields = ('alt_text',)

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price', 'is_active')
    list_filter = ('product', 'is_active')