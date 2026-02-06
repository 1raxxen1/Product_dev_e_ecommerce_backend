from django.contrib import admin
from .models import BlogPost , BlogCategory , BlogContentBlock , Keyword

# Register your models here.

# Category Model
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name','slug')
    search_fields = ('name',)

# Keyword Model
@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name','slug')
    search_fields = ('name',)

# Content Block Model
class BlogContentBlockInline(admin.TabularInline):
    model = BlogContentBlock
    extra = 1
    fields = ("block_type", "rich_text", "image", "order")
    ordering = ("order",)

# Blog Post Model
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'keywords')
    search_fields = ('title', 'excerpt')
    filter_horizontal = ('keywords',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogContentBlockInline]

