from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegisterForm, VerifyCodeForm, UserLoginForm
from random import randint
from utils import Send_OTP_code
from .models import OTPcode, User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegsiterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request,'you can\'t register now','danger')
            return redirect('home:homepage')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = UserRegisterForm()
        return render(request,'accounts/register.html',{'form':form})

    def post(self,request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            random_code = randint(1000,9999)
            Send_OTP_code(phone_number=form.cleaned_data['phone_number'], code=random_code)
            OTPcode.objects.create(phone_number=form.cleaned_data['phone_number'],code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'name': form.cleaned_data['name'],
                'password': form.cleaned_data['password']
            }
            messages.success(request, 'we sent you a code','success')
            return redirect('accounts:user_verify_code')
        return render(request,'accounts/register.html',{'form':form})


class UserVerifyCodeView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request,'you can\'t verify now','danger')
            return redirect('home:homepage')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = VerifyCodeForm()
        return render(request, 'accounts/verifycode.html',{'form':form})

    def post(self,request):
        user_session = request.session['user_registration_info']
        code_instance = OTPcode.objects.get(phone_number=user_session['phone_number'])
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            if code_instance.code == form.cleaned_data['code']:
                User.objects.create_user(name=user_session['name'],email=user_session['email'],
                                         password=user_session['password'],phone_number=user_session['phone_number'])
                code_instance.delete()
                messages.success(request,'you registered successfully','success')
                return redirect('home:homepage')
            else:
                messages.error(request,'This code is wrong','danger')
                return redirect('accounts:user_verify_code')
        return redirect('home:homepage')


class UserLoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request,'you can\'t login now','danger')
            return redirect('home:homepage')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = UserLoginForm()
        return render(request,'accounts/login.html',{'form':form})

    def post(self,request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, phone_number=data['phone_number'], password=data['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in successfully', 'success')
                return redirect('home:homepage')
            messages.error(request,'Phone Number or Password is wrong','danger')
        return render(request,'accounts/login.html',{'form':form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self,request):
        logout(request)
        messages.success(request,'you logged out successfully','success')
        return redirect('home:homepage')