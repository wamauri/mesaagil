from django.contrib import admin

from . import models

admin.site.register(models.Products)
admin.site.register(models.FoodImage)

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
    )
    list_display = list_fields
    list_display_links = list_fields
