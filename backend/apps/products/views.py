from unicodedata import category
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.postgres.search import SearchQuery , SearchRank
from django.db.models import F , Count , Min , Max , Avg

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
            .prefetch_related('images' , 'variants')
            .annotate(min_price=Min('variants__price'))
            
        )
        # Search and Filtering
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        if min_price:
            queryset = queryset.filter(variants__price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(variants__price__lte=max_price)
        
        if search:
            query = SearchQuery(search)
            queryset = (
                queryset
                .annotate(rank=SearchRank(F('search_vector'), query))
                .filter(rank__gte=0.1)
                .order_by('-rank')

            )

        ordering = self.request.query_params.get('ordering')
        if ordering == 'price_asc':
            queryset = queryset.order_by('min_price')

        elif ordering == 'price_desc':
            queryset = queryset.order_by('-min_price')
        
        elif ordering == 'newest':
            queryset = queryset.order_by('-created_at')

        elif ordering == 'oldest':
            queryset = queryset.order_by('created_at')
        
        else:
            queryset = queryset.order_by('-created_at')


        return queryset
    def list(self , request , *args , **kwargs):
        queryset = self.get_queryset()

        category_counts = (
            queryset
            .values('category__name', 'category__slug')
            .annotate(count=Count('id'))
            .order_by()
        )

        price_stats = (
            queryset
            .aggregate(
                min_price=Min('variants__price'),
                max_price=Max('variants__price'),
                avg_price=Avg('variants__price')
            )
        )

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return Response({
            "count": queryset.count(),
            "results": serializer.data,
            "filters": {
                "categories": list(category_counts),
                "price_range": price_stats
            }   
        })

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

#Admin Views

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




