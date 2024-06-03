from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Cart, CartItem, Order, OrderItem, Customer
from .forms import CartItemForm, OrderForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear perfil de cliente
            Customer.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}')
                return redirect('menu')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out')
    return redirect('home')

def menu(request):
    if not request.user.is_authenticated:
        return redirect('login')
    products = Product.objects.all()
    return render(request, 'core/menu.html', {'products': products})

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        # Asegurarse de que quantity tenga un valor por defecto de 1 si está vacío
        if not quantity:
            quantity = 1

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        
        # Obtener o crear un CartItem con un valor por defecto de 0 para quantity
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
        
        # Actualizar la cantidad del CartItem
        cart_item.quantity += int(quantity)
        cart_item.save()

        messages.success(request, f'Added {quantity} x {product.name} to your cart.')
        return redirect('menu')

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        return render(request, 'core/cart.html', {'cart': cart, 'step': 1})

    def post(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.cart = cart
            cart_item.save()
            return redirect('confirm_order')
        return render(request, 'core/cart.html', {'cart': cart, 'form': form, 'step': 1})


class ConfirmOrderView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        return render(request, 'core/confirm_order.html', {'cart': cart, 'step': 2})

    def post(self, request):
        # Aquí puedes añadir lógica adicional si es necesario
        return redirect('choose_delivery')


class ChooseDeliveryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'core/choose_delivery.html', {'step': 3})

    def post(self, request):
        choice = request.POST.get('delivery_choice')
        if choice == 'store':
            return redirect('payment')
        elif choice == 'home':
            return redirect('delivery_address')
        return render(request, 'core/choose_delivery.html', {'step': 3})

class DeliveryAddressView(LoginRequiredMixin, View):
    def get(self, request):
        form = OrderForm()
        return render(request, 'core/delivery_address.html', {'form': form, 'step': 3})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer
            order.status = 'pending'
            order.save()
            return redirect('payment')
        return render(request, 'core/delivery_address.html', {'form': form, 'step': 3})

class PaymentView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        return render(request, 'core/payment.html', {'cart': cart, 'step': 4})

    def post(self, request):
        cart = get_object_or_404(Cart, customer=request.user.customer)
        order = Order.objects.create(customer=request.user.customer, status='completed')
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        cart.delete()
        return render(request, 'core/order_confirmation.html', {'order': order, 'step': 4})

def order_confirmation(request):
    return render(request, 'core/order_confirmation.html')


class ConfirmOrderView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        return render(request, 'core/confirm_order.html', {'cart': cart, 'step': 2})

    def post(self, request):
        print("Confirm Order POST request received")
        return redirect('choose_delivery')
