from django import forms
from django.forms import widgets
from ebay.models import Product


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти",
                             widget=widgets.TextInput(attrs={
                                 'class': 'form-control me-2',
                                 'type': 'search',
                                 'placeholder': 'найти', 'aria-label': 'search'}))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price']
        widgets = {'description': widgets.Textarea(attrs={"cols": 24, "rows": 3, 'class': 'form-control'}),
                   'category': widgets.CheckboxSelectMultiple,
                   'name': widgets.TextInput(attrs={'class': 'form-control'})}
