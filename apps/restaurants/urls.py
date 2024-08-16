from django.urls import path

from . import views

urlpatterns = [
    path(route='waiters/new/', view=views.create_waiter, name='waiters-new' ),
    path(route='products/new/', view=views.create_products, name='products-new' ),
    path(route='image-product/new/<int:product_id>', view=views.upload_product_image, name='add-image-product' ),
    path(route='lobby/', view=views.lobby, name='lobby-chat' ),
    path(route='product/add/category/<int:product_id>', view=views.add_product_category, name='add-product-category'),
    path(route='category/<int:product_id>', view=views.add_category, name='add-category'),
]
