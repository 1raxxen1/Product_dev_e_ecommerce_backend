from django.urls import path
from . import views
from .views import (
    AdminReorderContentBlocksView,
    BlogPostListView,
    BlogPostDetailView, 
    BlogCategoryListView,
    BlogKeywordListView,
    AdminBlogPostCreateView,
    AdminBlogPostUpdateView,
    AdminBlogPostDeleteView,
    AdminContentBlockCreateView,
    AdminContentBlockUpdateView,
    AdminContentBlockDeleteView,
    AdminReorderContentBlocksView,

)
urlpatterns = [

    path("posts/", BlogPostListView.as_view()),
    path("posts/<slug:slug>/", BlogPostDetailView.as_view()),
    path("categories/", BlogCategoryListView.as_view()),
    path("keywords/", views.BlogKeywordListView.as_view()),
    
    path("admin/posts/", AdminBlogPostCreateView.as_view(), name="admin-blog-create"),
    path(
        "admin/posts/<int:pk>/",
        AdminBlogPostUpdateView.as_view(),
        name="admin-blog-update",
    ),
    path(
        "admin/posts/<int:pk>/delete/",
        AdminBlogPostDeleteView.as_view(),
        name="admin-blog-delete",
    ),

    path(
        "admin/blocks/",
        AdminContentBlockCreateView.as_view(),
        name="admin-block-create",
    ),
    path(
        "admin/blocks/<int:pk>/",
        AdminContentBlockUpdateView.as_view(),
        name="admin-block-update",
    ),
    path(
        "admin/blocks/<int:pk>/delete/",
        AdminContentBlockDeleteView.as_view(),
        name="admin-block-delete",
    ),

    path(
        "admin/posts/<int:post_id>/reorder-blocks/",
        AdminReorderContentBlocksView.as_view(),
        name="admin-reorder-blocks",
    ),

    
]


