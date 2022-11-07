from django.db import models
from accounts.models import User
from home.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)], blank=True,null=True,
                                   default=None)

    class Meta:
        ordering = ['paid']

    def __str__(self):
        return f'{self.user.name} - {self.updated} - {self.paid}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            total -= (self.discount * total)/100
        return int(total)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.order.user.name} - {self.product.name} - {self.quantity}'

    def get_cost(self):
        return self.quantity * self.price


class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
