from django import forms
from .models import CartItem, Order, Product

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']
