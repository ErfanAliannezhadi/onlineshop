from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'updated', 'paid']
    list_filter = ['paid']
    raw_id_fields = ['user']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon)