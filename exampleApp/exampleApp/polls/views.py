from django.core.paginator import Paginator
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
import json

from .serializers import *


def custom_paginator(contact_list, page_number, page_size):
    if page_number is None:
        page_number = 1

    if page_size is None:
        page_size = 2

    paginator = Paginator(contact_list, page_size)
    page_obj = paginator.get_page(page_number)

    return page_obj


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


@api_view(["PUT"])
def edit_product_of_brand(request, brand_id):
    Brand.objects.get(id=brand_id)
    data = json.loads(request.body)

    category_id = data.get('category')
    Category.objects.get(id=category_id)

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


@api_view(["GET"])
def get_products_details(request):
    store_id = request.GET.get('store_id')
    category_id = request.GET.get('category_id')

    products = Product.objects.all().only('id', 'name', 'brand', 'category', 'model_year')

    if store_id:
        products = products.filter(storeproduct__store_id=store_id)

    if category_id:
        products = products.filter(category_id=category_id)

    paginator = LimitOffsetPagination()

    paginated_products = paginator.paginate_queryset(products, request)

    serializer = ProductDetailSerializer(paginated_products, many=True)

    return Response(serializer.data)
