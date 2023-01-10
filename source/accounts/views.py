from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from accounts.forms import MyUserCreationForm
from accounts.models import Profile


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
