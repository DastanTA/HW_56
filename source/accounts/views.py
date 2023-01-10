from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from accounts.forms import MyUserCreationForm
from accounts.models import Profile
from ebay.models import OrderProduct


class RegisterView(CreateView):
    model = User
    template_name = 'registration/user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('task_tracker:project_main')
        return next_url


class MyOrdersView(LoginRequiredMixin, DetailView):
    template_name = 'orders.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = self.object.orders.filter(user=self.request.user)
        for order in orders:
            order_product = OrderProduct.objects.filter(order_id=order.pk)
            print(order_product)
        context['orders'] = orders
        return context
