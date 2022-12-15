from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView

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


class BasketView(ListView):
    model = Basket
    template_name = 'basket/in_basket.html'
    context_object_name = 'in_basket'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        total = 0
        for element in self.model.objects.all():
            total += element.get_product_total()
        form = OrderForm()
        context['total'] = total
        context['form'] = form
        return context


class InBasketDeleteView(DeleteView):
    model = Basket
    success_url = reverse_lazy('view_basket')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CreateOrder(View):
    def post(self, request, *args, **kwargs):
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
