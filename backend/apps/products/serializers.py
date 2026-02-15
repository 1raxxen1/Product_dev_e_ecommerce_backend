from rest_framework import serializers
from .models import (ProductCategory, Product, Variant, Inventory, ProductImage , ProductContentBlock)



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
    class Meta:
        model = Variant
        fields = ['id', 'name', 'price', 'sku', 'stock']

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

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'created_at', 'updated_at', 'is_active', 'images', 'content_blocks', 'variants']

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

