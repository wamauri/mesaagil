from django.contrib import admin

from . import models


@admin.register(models.Products)
class ProductsAdmin(admin.ModelAdmin):
    list_fields = (
        'id', 
        'name', 
        'description',
        'price',
        'category', 
        'food_image',
        'code',
        'created_at',
        'updated_at',
    )
    list_display = list_fields
    list_display_links = ('id', 'name')


@admin.register(models.FoodImage)
class FoodImageAdmin(admin.ModelAdmin):
    list_fields = (
        'id', 
        'image', 
        'thumbnail', 
        'code',
        'created_at',
        'updated_at',
    )
    list_display = list_fields
    list_display_links = ('id', 'image')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_fields = (
        'id', 
        'name', 
        'parent', 
        'lft',
        'rght',
        'tree_id',
        'level',
        'code',
        'created_at',
        'updated_at',
    )
    list_display = list_fields
    list_display_links = ('id', 'name')
