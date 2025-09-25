from django.db import models
from djago.contrib.auth.models import User
# Create your models here.

class Product(models.Model): 
    CATEGORY_CHOICE = [
        ("ayam", "Ayam"),  
        ("minuman", "Minuman"),
        ("lain", "Lainnya"),
    ]

    name        = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICE, default='ayam')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending","Pending"),
        ("processing","Processing"),
        ("done","Done"),
        ("cancelled","Cancelled"),
    ]

    user           = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    customer_email = models.EmailField()
    created_at     = models.DateTimeField(auto_now_add=True)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note           = models.TextField(blank=True)

    def total_amount(self):
        return sum(item.subtotal() for item in self.items.all())
    
    def __str__(self):
        return f"Order # {self.id} - {self.customer_email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} x{self.quantity}" 


