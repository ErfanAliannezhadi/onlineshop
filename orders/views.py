from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm, CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Coupon
from django.contrib import messages
from datetime import datetime


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request , product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.remove(product)
        return redirect('orders:cart')


class CreateOrderView(LoginRequiredMixin,View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order.id)


class OrderDetailView(LoginRequiredMixin,View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        form = CouponApplyForm()
        return render(request, 'orders/order.html', {'order': order, 'form': form})


class OrderPayView(View):
    def get(self, request, order_id):
        messages.error(request, 'This site is not connected to any payment gateway', 'danger')
        return redirect('orders:order_detail', order_id)


class CouponApplyView(View):
    def post(self, request, order_id):
        now = datetime.now()
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.warning(request,'this coupon does not exist','danger')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            return redirect('orders:order_detail', order_id)