from django.contrib import admin
from ebay.models import Product, Basket, Order, OrderProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category', 'remainder', 'price']
    list_filter = ['category']
    search_fields = ['name']


class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity']
    list_filter = ['quantity']
    search_fields = ['product']
    exclude = []


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'created_at', 'get_products']
    list_filter = ['created_at']
    search_fields = ['product', 'user_name']
    exclude = []
    filter_vertical = ['product']

    def get_products(self):
        for order in Order.objects.all():
            lst = []
            for prod in OrderProduct.objects.filter(order_id=order.pk):
                lst.append(prod.product)
            print(lst)
            return lst


admin.site.register(Product, ProductAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
