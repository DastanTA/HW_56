from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from ebay.models import Basket, Product, OrderProduct, Order


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


class BasketView(ListView):
    model = Basket
    template_name = 'basket/in_basket.html'
    context_object_name = 'in_basket'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        total = 0
        for element in self.model.objects.all():
            total += element.get_product_total()
        context['total'] = total
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
