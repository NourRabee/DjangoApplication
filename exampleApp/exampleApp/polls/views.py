from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
import json
from django.core import serializers


@csrf_exempt
def add_product_to_brand(request, brand_id):
    if request.method == 'POST':
        try:

            brand = Brand.objects.get(id=brand_id)

        except Brand.DoesNotExist:
            return JsonResponse({'error': 'brand not found'}, status=404)

        data = json.loads(request.body)
        category_id = data.get('category_id')

        if not category_id:
            return JsonResponse({'error': 'This category does not exist!'}, status=400)

        product = Product(name=data['name'], category_id=category_id, list_price=data['list_price'],
                          model_year=data['model_year'], brand=brand)
        product.save()

        data = serializers.serialize("json", [product])

        return JsonResponse({"data": json.loads(data)}, status=201)


def get_categories_of_certain_store(request, store_id):
    if request.method == 'GET':
        try:

            Store.objects.get(id=store_id)

        except Store.DoesNotExist:
            return JsonResponse({'error': 'Store not found'}, status=404)

        categories = Category.objects.filter(
            product__storeproduct__store_id=store_id
        ).distinct()

        data = serializers.serialize("json", categories)

        return JsonResponse({"data": json.loads(data)})


def get_categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        data = serializers.serialize("json", categories)
        return JsonResponse({"data": json.loads(data)})


def get_products_of_certain_store(request, store_id):
    if request.method == 'GET':

        try:

            Store.objects.get(id=store_id)

        except Store.DoesNotExist:
            return JsonResponse({'error': 'Store not found'}, status=404)

        products = Product.objects.filter(
            storeproduct__store_id=store_id
        )

        data = serializers.serialize("json", products)

        return JsonResponse({"data": json.loads(data)})


@csrf_exempt
def delete_product_from_store(request, store_id, product_id):
    if request.method == 'DELETE':

        try:

            Store.objects.get(id=store_id)
            Product.objects.get(id=product_id)

        except Store.DoesNotExist or Product.DoesNotExist:
            return JsonResponse({'error': 'Store or Product does not exist!'}, status=404)

        product = Product.objects.get(id=product_id, storeproduct__store_id=store_id)

        product.delete()

        return JsonResponse({'message': 'Products successfully deleted'}, status=204)
