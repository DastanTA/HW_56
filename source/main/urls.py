from django.contrib import admin
from django.urls import path
from ebay.views import AllProductsView, ProductView, ProductCreateView, ProductUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AllProductsView.as_view(), name='all_products'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/', ProductView.as_view(), name='view_product'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),
]
