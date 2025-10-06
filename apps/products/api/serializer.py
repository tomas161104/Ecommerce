from rest_framework import serializers
from apps.products.models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'stock', 'img']

        read_only_fields= ['created_at', 'category']