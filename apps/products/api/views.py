from rest_framework.viewsets import ModelViewSet
from apps.products.models import Product, Category
from .serializer import ProductSerializer, CategorySerializer
from .permissions import IsAdminUserOrReadOnly

class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()




class ProductViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()