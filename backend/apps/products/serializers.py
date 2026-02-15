from rest_framework import serializers
from .models import (ProductCategory, Product, Variant, Inventory, ProductImage , ProductContentBlock)
from django.db.models import Min



class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'parent']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'alt_text', 'order']

class ProductContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductContentBlock
        fields = ['id', 'product', 'block_type', 'content', 'order']

class ProductVariantSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory.stock', read_only=True)
    in_stock = serializers.BooleanField(source="in_stock", read_only=True)
    class Meta:
        model = Variant
        fields = ['id', 'name', 'price', 'sku', 'stock', 'in_stock']

class ProductListSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'created_at', 'updated_at', 'is_active' , 'slug' , 'images' , 'variants']

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    content_blocks = ProductContentBlockSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'created_at', 'updated_at', 'is_active']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    content_blocks = ProductContentBlockSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    in_stock = serializers.BooleanField(source="in_stock", read_only=True)

    def get_queryset(self):
        queryset = (
            Product.objects
            .filter(is_active=True)
            .select_related('category') 
            .prefetch_related('images' , 'content_blocks', 'variants__inventory')
            .annotate(min_price=Min('variants__price'))
        )
        return queryset

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'created_at', 'updated_at', 'is_active', 'images', 'min_price', 'content_blocks', 'variants', 'in_stock']

class ProductAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'created_at', 'updated_at', 'is_active' , 'slug']

class ProductImageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'alt_text', 'order']

class ProductContentBlockAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductContentBlock
        fields = ['id', 'product', 'block_type', 'content', 'image', 'order']

class ProductVariantAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'product', 'name', 'price', 'sku', 'is_active']

class InventoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'variant', 'stock', 'updated_at']

