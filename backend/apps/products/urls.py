from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # 🛍 PUBLIC APIs
    # =========================

    path("products/", views.ProductListView.as_view()),
    path("products/<slug:slug>/", views.ProductDetailView.as_view()),
    path("categories/", views.ProductCategoryListView.as_view()),


    # =========================
    # 🔐 ADMIN APIs
    # =========================

    # Product CRUD
    path("admin/products/create/", views.ProductAdminCreateView.as_view()),
    path("admin/products/<int:pk>/update/", views.ProductAdminUpdateView.as_view()),
    path("admin/products/<int:pk>/delete/", views.ProductAdminDeleteView.as_view()),

    # Images
    path("admin/images/create/", views.AdminProductImageCreateView.as_view()),
    path("admin/images/<int:pk>/update/", views.AdminProductImageUpdateView.as_view()),
    path("admin/images/<int:pk>/delete/", views.AdminProductImageDeleteView.as_view()),

    # Content Blocks
    path("admin/blocks/create/", views.AdminProductContentBlockCreateView.as_view()),
    path("admin/blocks/<int:pk>/update/", views.AdminProductContentBlockUpdateView.as_view()),
    path("admin/blocks/<int:pk>/delete/", views.AdminProductContentBlockDeleteView.as_view()),
    path("admin/products/<int:product_id>/reorder-blocks/", views.AdminReorderProductContentBlocksView.as_view()),

    # Variants
    path("admin/variants/create/", views.AdminProductVariantCreateView.as_view()),
    path("admin/variants/<int:pk>/update/", views.AdminProductVariantUpdateView.as_view()),
    path("admin/variants/<int:pk>/delete/", views.AdminProductVariantDeleteView.as_view()),

    # Inventory
    path("admin/inventory/<int:pk>/update/", views.AdminInventoryUpdateView.as_view()),
]

