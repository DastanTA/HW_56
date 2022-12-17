from django.contrib import admin
from django.urls import path
from ebay.views import AllProductsView, ProductView, ProductCreateView,\
    ProductUpdateView, ProductDeleteView, AddToBasketView, BasketView, \
    InBasketDeleteView, CreateOrder, BasketDeleteOneView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AllProductsView.as_view(), name='all_products'),
    path('add_order/', CreateOrder.as_view(), name='add_order'),
    path('basket/', BasketView.as_view(), name='view_basket'),
    path('basket/<int:pk>/delete', InBasketDeleteView.as_view(), name='delete_in_basket'),
    path('basket/<int:pk>/delete_one', BasketDeleteOneView.as_view(), name='delete_one_in_basket'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/', ProductView.as_view(), name='view_product'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pk>/add_to_basket', AddToBasketView.as_view(), name='add_to_basket'),
]
