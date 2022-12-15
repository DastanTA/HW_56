from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from ebay.models import Basket, Product, OrderProduct, Order
from ebay.forms import OrderForm


class AddToBasketView(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        try:
            basket = Basket.objects.get(product=product)
        except Basket.DoesNotExist:
            if product.remainder > 0:
                Basket.objects.create(product=product, quantity=1)
        else:
            if basket.quantity < product.remainder:
                basket.quantity += 1
                basket.save()
        return redirect('all_products')


class BasketView(TemplateView):
    template_name = 'basket/in_basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = OrderForm()
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
        context['form'] = form
        return context


class InBasketDeleteView(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        prod_in_basket = Basket.objects.get(product=product)
        prod_in_basket.delete()
        return redirect('view_basket')


class CreateOrder(View):
    def post(self, request, *arg, **kwargs):
        in_basket = Basket.objects.all()
        user_namee = self.request.POST.get('user_name')
        adress = self.request.POST.get('address')
        phone_n = self.request.POST.get('phone')
        order = Order.objects.create(user_name=user_namee, address=adress, phone=phone_n)

        for element in in_basket:
            OrderProduct.objects.create(order=order, product=element.product, quantity=element.quantity)

        for element1 in in_basket:
            element1.delete()
        return redirect('view_basket')
