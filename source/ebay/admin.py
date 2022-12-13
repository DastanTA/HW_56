from django.contrib import admin
from ebay.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category', 'remainder', 'price']
    list_filter = ['category']
    search_fields = ['name']
    exclude = []


admin.site.register(Product, ProductAdmin)
