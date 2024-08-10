from django.core.paginator import Paginator
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
import json


def custom_paginator(contact_list, page_number, page_size):
    if page_number is None:
        page_number = 1

    if page_size is None:
        page_size = 2

    paginator = Paginator(contact_list, page_size)
    page_obj = paginator.get_page(page_number)

    return page_obj


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'model_year', 'list_price']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


@api_view(["POST", "PUT"])
def add_product_to_brand(request, brand_id):
    Brand.objects.get(id=brand_id)
    data = json.loads(request.body)

    category_id = data.get('category')
    Category.objects.get(id=category_id)

    if request.method == 'POST':

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['brand_id'] = brand_id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':

        product_id = request.GET.get('product_id')

        product = Product.objects.get(id=product_id)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_categories_of_certain_store(request, store_id):
    Store.objects.get(id=store_id)

    categories = Category.objects.filter(
        product__storeproduct__store_id=store_id
    ).distinct()

    # # Get the page number from the request
    page_number = request.GET.get('page')
    per_page = request.GET.get('page_size')

    serializer = CategorySerializer(custom_paginator(categories, page_number, per_page), many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_categories(request):
    categories = Category.objects.all()

    # Get the page number from the request
    page_number = request.GET.get('page')
    per_page = request.GET.get('page_size')

    serializer = CategorySerializer(custom_paginator(categories, page_number, per_page), many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_products_of_certain_store(request, store_id):
    Store.objects.get(id=store_id)

    products = Product.objects.filter(
        storeproduct__store_id=store_id
    )

    page_number = request.GET.get('page')
    per_page = request.GET.get('page_size')

    serializer = CategorySerializer(custom_paginator(products, page_number, per_page), many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_product_from_store(request, store_id, product_id):
    Store.objects.get(id=store_id)
    Product.objects.get(id=product_id)

    product = Product.objects.get(id=product_id, storeproduct__store_id=store_id)

    product.delete()

    return Response({'message': 'Products successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
