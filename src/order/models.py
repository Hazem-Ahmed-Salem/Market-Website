from django.db import models
from product.models import Product
from user.models import CustomUser,Address
from decimal import Decimal

# Create your models here.


class CartItem(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    order_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def order_vat(self):
        return self.price_per_unit * self.quantity * Decimal(0.2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'product_image': self.product.image.url,
            'product_name': self.product.name,
            'product_description': self.product.description,
            'product_category': self.product.category.name if self.product.category else None,
            'product_price': float(self.product.price),
            'quantity': self.quantity,
            'price_per_unit': float(self.price_per_unit),
            'order_price': (float(self.price_per_unit) * float(self.quantity)) + float(self.order_vat()),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self):
        return f"{self.customer}:{self.product}:{self.quantity} id:{self.id}"


class Order(models.Model):
    Status_choices = [
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled'),
    ]
    Payment_choices = [
        ('cash_on_delivery','Cash on delivery'),
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.JSONField(default=list)
    order_vat = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    order_price_without_vat = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    order_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255,choices=Status_choices,default='pending')
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True,default=None)
    payment_method = models.CharField(max_length=255,choices=Payment_choices,default='cash_on_delivery')

    def order_total(self):
        return float(self.order_price + self.order_vat())
    def __str__(self):
        return f"{self.customer}"

class Sales(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.JSONField(default=list)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)  
    
    
    def __str__(self):
        return f"{self.order}"

