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
        flag = False
        for element in Basket.objects.all():
            if product == element.product:
                flag = True
            else:
                continue

        if not flag:
            Basket.objects.create(product=product, quantity=1)
            print(product)
            return redirect('all_products')
        elif flag:
            product_to_update = Basket.objects.get(product=product)
            if product_to_update.quantity < product.remainder:
                product_to_update.quantity = product_to_update.quantity + 1
                product_to_update.save()
                return redirect('all_products')
            else:
                return redirect('all_products')
