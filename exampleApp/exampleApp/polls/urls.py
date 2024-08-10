from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls

from . import views

urlpatterns = [
    # The ability to add a products to a certain brand
    # post api/brands/{brand_id}/products
    path('brands/<int:brand_id>/products', views.add_product_to_brand),

    # Get all the categories that exist for certain store
    # GET stores/{store_id}/products/categories
    path('stores/<int:store_id>/products/categories', views.get_categories_of_certain_store),

    # Get a list of the all the categories in the website
    # Get api/categories
    path('categories', views.get_categories),

    # Get all products details for a certain store
    # Get api/stores/{store_id}/products
    path('stores/<int:store_id>/products', views.get_products_of_certain_store),

    # Delete a product for a certain store
    # Delete api/stores/{store_id}/products/{product_id}
    path('stores/<int:store_id>/products/<int:product_id>', views.delete_product_from_store),
] + debug_toolbar_urls()
