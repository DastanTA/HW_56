from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from ebay.models import Product, CATEGORY_CHOICES
from ebay.views.base_views import SearchView
from ebay.forms import ProductForm

Product.objects.all().order_by("category", "name").filter(remainder__gt=0)


class AllProductsView(SearchView):
    model = Product
    ordering = ['category', 'name']
    template_name = 'products/index.html'
    context_object_name = 'products'
    paginate_by = 5
    paginate_orphans = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(remainder__gt=0)

    def get_query(self):
        query = Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value)
        return query


class ProductView(DetailView):
    model = Product
    template_name = 'products/product.html'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'products/create_product.html'
    form_class = ProductForm
