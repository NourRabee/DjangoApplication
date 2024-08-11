from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'model_year', 'list_price']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'phone', 'email', 'street', 'city', 'state', 'zip_code']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    store = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'category', 'model_year', 'store']

    def get_store(self, obj):

        store_products = StoreProduct.objects.filter(product=obj).select_related('store')

        serialized_stores = []

        for store_product in store_products:
            store_data = StoreSerializer(store_product.store).data

            serialized_stores.append({
                'store': store_data
            })

        return serialized_stores
