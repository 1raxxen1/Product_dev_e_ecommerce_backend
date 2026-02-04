from django.urls import path
from . import views
from .views import BlogPostListView, BlogPostDetailView, BlogCategoryListView

urlpatterns = [

    path("posts/", BlogPostListView.as_view()),
    path("posts/<slug:slug>/", BlogPostDetailView.as_view()),
    path("categories/", BlogCategoryListView.as_view()),
    
]


