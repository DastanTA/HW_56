from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from ebay.models import Basket, Product


class AddToBasketView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        product = Product.objects.get(pk=pk)
        context = {'product': product}
        return render(request, 'basket/add_to_basket.html', context)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        product = Product.objects.get(pk=pk)
        if product not in Basket.objects.all():
            Basket.objects.create(product=product, quantity=1)
            return redirect('all_products')
        else:
            qnt = Basket.objects.get(product).quantity
            if qnt < product.remainder:
                Basket.objects.get(product).quantity = qnt + 1
                return redirect('all_products')
            else:
                return redirect('all_products')
