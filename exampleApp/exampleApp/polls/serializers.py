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
        # Get all StoreProduct entries related to the given product
        store_products = StoreProduct.objects.filter(product=obj).select_related('store')

        serialized_stores = []

        for store_product in store_products:
            store_data = StoreSerializer(store_product.store).data

            serialized_stores.append({
                'store': store_data
            })

        return serialized_stores


class ProductFromDictSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    brand = serializers.IntegerField()
    category = serializers.IntegerField()
    model_year = serializers.IntegerField()

    def create(self, validated_data):
        return Product(
            id=validated_data['id'],
            name=validated_data['name'],
            brand_id=validated_data['brand'],
            category_id=validated_data['category'],
            model_year=validated_data['model_year']
        )
