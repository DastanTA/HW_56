from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from ebay.models import Product, Basket


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти",
                             widget=widgets.TextInput(attrs={
                                 'class': 'form-control me-2',
                                 'type': 'search',
                                 'placeholder': 'найти', 'aria-label': 'search'}))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'remainder']
        widgets = {'description': widgets.Textarea(attrs={"cols": 24, "rows": 3, 'class': 'form-control'}),
                   'category': widgets.RadioSelect,
                   'name': widgets.TextInput(attrs={'class': 'form-control'})}
        error_messages = {
            'name': {'required': "Нельзя оставлять название пустым!"},
            'price': {'max_digits': "не больше 7 знаков!"},
            'remainder': {'positive': "Остаток не может быть ниже нуля!"}
        }

    def clean_remainder(self):
        remainder = self.cleaned_data.get('remainder')
        if remainder < 0:
            raise ValidationError('Остаток не может быть ниже нуля!')
        return remainder

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError('Цена не может быть ниже 0!')
        return price


