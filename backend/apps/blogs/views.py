from django.shortcuts import render
from rest_framework import generics
from .models import BlogPost, BlogCategory , BlogContentBlock , Keyword
from .serializers import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogCategorySerializer,
    BlogContentBlockSerializer,
    BlogkeywordSerializer,
    BlogPostAdminSerializer,
)

# Create your views here.

class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(is_published=True).order_by("-created_at")
    serializer_class = BlogPostListSerializer


class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostDetailSerializer
    lookup_field = "slug"


class BlogCategoryListView(generics.ListAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer

