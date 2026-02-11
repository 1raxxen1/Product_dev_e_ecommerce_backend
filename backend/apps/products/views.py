from unicodedata import category
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Product,
    ProductCategory,
    ProductImage,
    ProductContentBlock,
    Variant,
    Inventory,
)

from .serializers import (
    ProductCategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductAdminSerializer,
    ProductImageAdminSerializer,
    ProductContentBlockAdminSerializer,
    ProductVariantAdminSerializer,
    InventoryAdminSerializer,
)


# Create your views here.

class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset =(
            Product.objects
            .filter(is_active=True)
            .select_related('category') 
            .prefetch_related('images')
            .order_by('-created_at')
        )
        

        category = self.request.query_params.get('category')

        if category:
                queryset = queryset.filter(category__slug=category)

        return queryset

class ProductDetailView(generics.RetrieveAPIView):
     serializer_class = ProductDetailSerializer
     lookup_field = 'slug'

     def get_queryset(self):
          return (
               Product.objects
               .filter(is_active=True)
                .select_related('category')
                .prefetch_related(
                    'images',
                    'content_blocks',
                    'variants__inventory'
                )
            )

class ProductCategoryListView(generics.ListAPIView):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()

class ProductAdminCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductAdminSerializer
    queryset = Product.objects.all()

class ProductAdminUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductAdminSerializer
    queryset = Product.objects.all()

class ProductAdminDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductAdminSerializer
    queryset = Product.objects.all()

class AdminProductImageCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductImageAdminSerializer


class AdminProductImageUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageAdminSerializer


class AdminProductImageDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageAdminSerializer

class AdminProductContentBlockCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductContentBlockAdminSerializer


class AdminProductContentBlockUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = ProductContentBlock.objects.all()
    serializer_class = ProductContentBlockAdminSerializer


class AdminProductContentBlockDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = ProductContentBlock.objects.all()
    serializer_class = ProductContentBlockAdminSerializer

class AdminReorderProductContentBlocksView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, product_id):
        for item in request.data:
            ProductContentBlock.objects.filter(
                id=item["block_id"],
                product_id=product_id
            ).update(order=item["order"])

        return Response({"status": "ok"}, status=status.HTTP_200_OK)

class AdminProductVariantCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductVariantAdminSerializer


class AdminProductVariantUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Variant.objects.all()
    serializer_class = ProductVariantAdminSerializer


class AdminProductVariantDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Variant.objects.all()
    serializer_class = ProductVariantAdminSerializer

class AdminInventoryUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Inventory.objects.all()
    serializer_class = InventoryAdminSerializer




