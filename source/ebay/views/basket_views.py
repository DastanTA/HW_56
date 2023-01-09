from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DeleteView, CreateView

from ebay.models import Basket, Product, Order, OrderProduct
from ebay.forms import OrderForm


class AddToBasketView(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        qty = int(request.POST.get('quantity'))

        basket, _ = Basket.objects.get_or_create(product=product, quantity=0)

        if product.remainder >= basket.quantity + qty:
            basket.quantity += qty
            basket.save()
        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        else:
            return reverse('ebay:all_products')


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
    success_url = reverse_lazy('ebay:view_basket')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class BasketDeleteOneView(DeleteView):
    model = Basket
    success_url = reverse_lazy('ebay:view_basket')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.quantity -= 1
        if self.object.quantity < 1:
            self.object.delete()
        else:
            self.object.save()
        return redirect(success_url)


class CreateOrder(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('ebay:all_products')

    def form_valid(self, form):
        order = form.save()

        for item in Basket.objects.all():
            OrderProduct.objects.create(product=item.product, quantity=item.quantity, order=order)
            item.product.remainder -= item.quantity
            item.product.save()
            item.delete()

        return redirect(self.success_url)
