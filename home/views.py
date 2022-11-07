from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Product
from .tasks import all_bucket_objects_task, delete_object_task, download_object_task
from django.contrib import messages
from utils import IsUserAdminMixin
from orders.forms import CartAddForm


class HomeView(View):
    def get(self,request):
        categories = Category.objects.filter(is_sub=False)
        products = Product.objects.all()
        return render(request,'home/homepage.html',{'categories': categories, 'products': products})


class CategoryView(View):
    def get(self, request, category_slug):
        products = Product.objects.filter(available=True)
        categories = Category.objects.all()
        category = [category for category in categories if category.slug == category_slug][0]
        products = products.filter(category=category)
        categories = Category.objects.filter(is_sub=False)
        return render(request, 'home/category_detail.html', {'products': products, 'categories': categories})


class ProductView(View):
    def get(self, request, product_slug):
        products = Product.objects.all()
        product = [product for product in products if product.slug == product_slug][0]
        form = CartAddForm()
        return render(request,'home/product.html',{'product':product, 'form': form})


class BucketView(IsUserAdminMixin, View):
    def get(self, request):
        objects = all_bucket_objects_task()
        return render(request, 'home/bucket.html', {'objects': objects})


class BucketObjectDeleteView(IsUserAdminMixin, View):
    def get(self, request, key):
        delete_object_task.delay(key)
        messages.success(request, 'This object will be deleted soon', 'info')
        return redirect('home:bucket')


class BucketObjectDownloadView(IsUserAdminMixin, View):
    def get(self, request, key):
        download_object_task.delay(key)
        messages.success(request, 'your download will start soon', 'info')
        return redirect('home:bucket')