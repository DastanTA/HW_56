from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from accounts.views import RegisterView, MyOrdersView


app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/orders/', MyOrdersView.as_view(), name='view_orders'),
]
