from django.http import JsonResponse
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
import json


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'model_year', 'list_price']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


@api_view(["POST"])
def add_product_to_brand(request, brand_id):
    Brand.objects.get(id=brand_id)
    data = json.loads(request.body)

    category_id = data.get('category')
    Category.objects.get(id=category_id)

    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.validated_data['brand_id'] = brand_id
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_categories_of_certain_store(request, store_id):
    Store.objects.get(id=store_id)

    categories = Category.objects.filter(
        product__storeproduct__store_id=store_id
    ).distinct()

    serializer = CategorySerializer(categories, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_products_of_certain_store(request, store_id):
    Store.objects.get(id=store_id)

    products = Product.objects.filter(
        storeproduct__store_id=store_id
    )

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_product_from_store(request, store_id, product_id):
    Store.objects.get(id=store_id)
    Product.objects.get(id=product_id)

    product = Product.objects.get(id=product_id, storeproduct__store_id=store_id)

    product.delete()

    return Response({'message': 'Products successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
