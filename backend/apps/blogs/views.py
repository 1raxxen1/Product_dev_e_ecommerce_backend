from django.shortcuts import render
from rest_framework import generics , status
from rest_framework.response import Response
from rest_framework.views import APIView
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
    serializer_class = BlogPostListSerializer

    def get_queryset(self):
        qs = (
            BlogPost.objects.filter(is_published=True)
            .select_related("category")
            .prefetch_related("keywords")
            .order_by("-created_at")
        )

        category = self.request.query_params.get("category")
        keyword = self.request.query_params.get("keyword")

        if category:
            qs = qs.filter(category__slug=category)
        if keyword:
            qs = qs.filter(keywords__slug=keyword)

        return qs


class BlogPostDetailView(generics.RetrieveAPIView):
    serializer_class = BlogPostDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            BlogPost.objects.filter(is_published=True)
            .select_related("category")
            .prefetch_related("keywords", "content_blocks")
        )
    


class BlogCategoryListView(generics.ListAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer

class BlogKeywordListView(generics.ListAPIView):
    queryset = Keyword.objects.all()
    serializer_class = BlogkeywordSerializer


# Admin Views

class AdminBlogPostCreateView(generics.CreateAPIView):
    permission_classes = []  # Add appropriate permissions
    serializer_class = BlogPostAdminSerializer

class AdminBlogPostUpdateView(generics.UpdateAPIView):
    permission_classes = []  # Add appropriate permissions
    serializer_class = BlogPostAdminSerializer
    queryset = BlogPost.objects.all()
    lookup_field = "id"

class AdminBlogPostDeleteView(generics.DestroyAPIView):
    permission_classes = []  # Add appropriate permissions
    queryset = BlogPost.objects.all()
    lookup_field = "id"

class AdminBlogCategoryCreateView(generics.CreateAPIView):
    permission_classes = []  # Add appropriate permissions
    serializer_class = BlogCategorySerializer

class AdminBLogCategoryDeleteView(generics.DestroyAPIView):
    permission_classes = []  # Add appropriate permissions
    queryset = BlogCategory.objects.all()
    lookup_field = "id"

class AdminContentBlockCreateView(generics.CreateAPIView):
    permission_classes = []  # Add appropriate permissions
    serializer_class = BlogContentBlockSerializer

class AdminContentBlockUpdateView(generics.UpdateAPIView):
    permission_classes = []  # Add appropriate permissions
    serializer_class = BlogContentBlockSerializer
    queryset = BlogContentBlock.objects.all()
    lookup_field = "id"

class AdminContentBlockDeleteView(generics.DestroyAPIView):
    permission_classes = []  # Add appropriate permissions
    queryset = BlogContentBlock.objects.all()
    lookup_field = "id"

class AdminReorderContentBlocksView(generics.UpdateAPIView):
    permission_classes = []  # Add appropriate permissions
    
    def post(self, request, post_id):
       for item in request.data:
            BlogContentBlock.objects.filter(
                id=item["block_id"],
                blog_post_id=post_id
            ).update(order=item["order"])
        
            return Response({"status": "success"} , status=status.HTTP_200_OK)

