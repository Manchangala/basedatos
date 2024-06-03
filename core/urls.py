from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('confirm_order/', views.ConfirmOrderView.as_view(), name='confirm_order'),
    path('choose_delivery/', views.ChooseDeliveryView.as_view(), name='choose_delivery'),
    path('delivery_address/', views.DeliveryAddressView.as_view(), name='delivery_address'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),

    # URLs para la sección de administración personalizada
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/products/', views.admin_products, name='admin_products'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/reports/', views.admin_reports, name='admin_reports'),
]


