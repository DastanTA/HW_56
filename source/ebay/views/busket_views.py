from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView

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
            return redirect('all_products')
        elif flag:
            product_to_update = Basket.objects.get(product=product)
            if product_to_update.quantity < product.remainder:
                product_to_update.quantity = product_to_update.quantity + 1
                product_to_update.save()
                return redirect('all_products')
            else:
                return redirect('all_products')


class BasketView(TemplateView):
    template_name = 'basket/in_basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        in_basket = Basket.objects.all()
        all_products = Product.objects.all()
        prod_sum_dict = {}
        total = 0
        for element in in_basket:
            price = all_products.get(name__iexact=element.product.name).price
            summ = element.quantity * price
            prod_sum_dict[element.product.name] = summ
            total += summ
        context['sum'] = prod_sum_dict
        context['in_basket'] = in_basket
        context['total'] = total
        return context


class InBasketDeleteView(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        prod_in_basket = Basket.objects.get(product=product)
        prod_in_basket.delete()
        return redirect('view_basket')
