from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import Group
from .models import User, OTPcode


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['name','email','phone_number','is_admin']
    list_filter = ['is_admin']
    readonly_fields = ['last_login']
    fieldsets = [
        [None,{'fields':['name','password','phone_number','email']}],
        ['Permissions', {'fields':['is_active','is_admin','is_superuser','last_login','groups','user_permissions']}]
    ]
    add_fieldsets = [
        [None, {'fields':['name','phone_number','email','password1','password2']}]
    ]
    search_fields = ['email','name']
    ordering = ['name']
    filter_horizontal = ['user_permissions','groups']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


class OTPcodeAdmin(admin.ModelAdmin):
    list_display = ['phone_number','code','created']


admin.site.register(User,UserAdmin)
admin.site.register(OTPcode, OTPcodeAdmin)