from rest_framework import serializers
from .models import BlogPost , BlogCategory , BlogContentBlock , Keyword

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug']

class BlogkeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name', 'slug']

class BlogContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogContentBlock
        fields = ['id', 'block_type', 'rich_text', 'image', 'order']

class BlogPostListSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt',
            'cover_image', 'category', 'keywords', 'created_at'
        ]

class BlogPostDetailSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer()
    keywords = BlogkeywordSerializer(many=True, read_only=True)
    content_blocks = BlogContentBlockSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'cover_image',
            'category', 'keywords', 'content_blocks', 'created_at'
        ]
class BlogPostAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields =[
            "id",
            "title",
            "slug",
            "excerpt",
            "cover_image",
            "category",
            "keywords",
            "is_published",
        ]
