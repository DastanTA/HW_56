from django.contrib import admin
from django.urls import path
from ebay.views import AllProductsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AllProductsView.as_view(), name='all_products'),
]
