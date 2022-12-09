from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from ebay.models import Product, CATEGORY_CHOICES
from ebay.views.base_views import SearchView

Product.objects.all().order_by("category", "name").filter(remainder__gt=0)


class AllProductsView(SearchView):
    model = Product
    ordering = ['category', 'name']
    template_name = 'products/index.html'
    context_object_name = 'products'
    paginate_by = 50
    paginate_orphans = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(remainder__gt=0)

    def get_query(self):
        query = Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value) | Q(project__title__icontains=self.search_value)
        return query
