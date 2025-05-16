from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    Shelf_life_choices = [
    ('p', 'Perishable'),
    ('n', 'Non-Perishable'),
    ]
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=None,null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    volume = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    shelf_life = models.CharField(max_length=255,choices=Shelf_life_choices)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    is_published = models.BooleanField(default=False)
    wishlist = models.ManyToManyField(User, related_name='wishlist_products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def has_stock(self):
        return self.get_stock_quantity()>0
    def format_data_price_predictor(self):
        return {
            'name': self.name,
            'Weight_Volume': self.to_grams(),
            'category': self.category.name,
            'date': self.created_at.date(),
            'price': self.price,
            'shelf_life': self.get_shelf_life_value(),
        }
    
    def get_shelf_life_value(self):
        for code, value in self.Shelf_life_choices:
            if code == self.shelf_life:
                return value
        return None
    
    def to_grams(self):
        if self.category.name == 'Dairy' or self.category.name == 'Beverages':
            return float(self.volume * 1000)
        else:
            return float(self.weight * 1000)
    @classmethod
    def get_category_choices(cls):
        return Category.objects.filter(is_published=True)
    @classmethod
    def get_shelf_life_choices(cls):
        return [choice[1] for choice in cls.Shelf_life_choices]

    def get_stock_quantity(self):
        return Stock.objects.filter(product=self.id).aggregate(models.Sum('quantity'))['quantity__sum'] or 0
    
    def get_stock_status(self):
        return self.get_stock_quantity() > 0
    
    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.product}:{self.quantity} Units".title()


    


