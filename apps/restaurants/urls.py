from django.urls import path

from . import views

urlpatterns = [
    path(route='waiters/new/', view=views.create_waiter, name='waiters-new' ),
    path(route='products/new/', view=views.create_products, name='products-new' )
]
