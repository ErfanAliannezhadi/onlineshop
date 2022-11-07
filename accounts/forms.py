from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import OTPcode


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email','name','phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('Passwords don\'t match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change the password using '
                                                   '<a href=\"../password/\">this form</a>.')

    class Meta:
        model = User
        fields = ['email','phone_number','name','password','last_login']
        widgets ={
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class UserRegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control'}),label='Phone Number')
    password = forms.CharField( widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        OTPcode.objects.filter(phone_number=phone_number).delete()
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('This phone number already exists')
        return phone_number


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),label='Phone Number')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))