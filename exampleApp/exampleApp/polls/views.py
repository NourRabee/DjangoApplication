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
    try:
        Brand.objects.get(id=brand_id)
    except Brand.DoesNotExist:
        return JsonResponse({'error': 'brand not found'}, status=status.HTTP_404_NOT_FOUND)

    data = json.loads(request.body)
    category_id = data.get('category')

    try:
        Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'brand not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['brand_id'] = brand_id
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_categories_of_certain_store(request, store_id):
    try:

        Store.objects.get(id=store_id)

    except Store.DoesNotExist:
        return JsonResponse({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

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
    try:

        Store.objects.get(id=store_id)

    except Store.DoesNotExist:
        return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

    products = Product.objects.filter(
        storeproduct__store_id=store_id
    )

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_product_from_store(request, store_id, product_id):
    try:

        Store.objects.get(id=store_id)
        Product.objects.get(id=product_id)

    except Store.DoesNotExist or Product.DoesNotExist:
        return Response({'error': 'Store or Product does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    product = Product.objects.get(id=product_id, storeproduct__store_id=store_id)

    product.delete()

    return Response({'message': 'Products successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
