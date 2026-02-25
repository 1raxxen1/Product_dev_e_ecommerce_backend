from django.contrib import admin
from django.db.models import Min
from .models import Product, ProductCategory, ProductImage, Variant

class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# Register your models here.
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status')
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "description", "category", "status", "meta_title", "meta_description", "meta_keywords")
        }),
        ("SEO Info", {
            "fields": ("slug",)
        })
    )
    list_filter = ('category', 'status', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [VariantInline, ProductImageInline]
    exclude = ('search_vector',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(min_price=Min('variants__price'))

    def get_min_price(self, obj):
        return obj.min_price
    get_min_price.short_description = "Min Price"

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_url', 'alt_text', 'order')
    list_filter = ('product',)
    search_fields = ('alt_text',)

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price', 'is_active')
    list_filter = ('product', 'is_active')


