from django.db import models
from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

class PlannerTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    task = models.CharField(max_length=255)
    date = models.DateField(default=date.today)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task

# Create your models here.
from django.db import models
from datetime import timedelta, date

FREQUENCY_CHOICES = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
]


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    frequency = models.CharField(
        max_length=20,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        default='daily'
    )
    start_date = models.DateField(default=date.today)

    def next_due_date(self):
        delta = {'daily': 1, 'weekly': 7, 'monthly': 30}.get(self.frequency, 1)
        return self.start_date + timedelta(days=delta)


class Spending(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} - ₹{self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.category} - ₹{self.amount}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')  # Store in media/

    def __str__(self):
        return f"{self.name} ({self.category})"
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity
