from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, CreateView

from ebay.models import Basket, Product, Order, OrderProduct
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
        context['total'] = total
        context['form'] = OrderForm()
        return context


class InBasketDeleteView(DeleteView):
    model = Basket
    success_url = reverse_lazy('view_basket')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CreateOrder(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('all_products')

    def form_valid(self, form):
        order = form.save()

        for item in Basket.objects.all():
            OrderProduct.objects.create(product=item.product, quantity=item.quantity, order=order)
            item.product.remainder -= item.quantity
            item.product.save()
            item.delete()

        return redirect(self.success_url)
