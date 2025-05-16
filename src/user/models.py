from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self,first_name,last_name, email,user_role='customer', password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name,last_name=last_name,email=email,user_role=user_role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name,last_name, email,user_role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(first_name,last_name,email,user_role, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    choices = [('manager', 'Manager'), ('employee', 'Employee'), ('inventory_manager', 'Inventory Manager'), ('driver', 'Driver'),('customer', 'Customer')]
    user_role = models.CharField(max_length=20, choices=choices)

    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','user_role']
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.email

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address_type_choices = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]
    address_type = models.CharField(max_length=100, choices=address_type_choices, default='home')
    address = models.TextField()
    apartment = models.CharField(max_length=100,default='Apartment')
    city = models.CharField(max_length=100)
    governorate = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.governorate}"

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10,choices=[('male','Male'),('female','Female'),('other','Other')],default='male')
    phone_number = models.CharField(max_length=10)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,default=None,null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default_profile.png')

    def __str__(self):
        return self.user.email

class TechnicalComplaint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=100, choices=[
        ('website', 'Website Problem'),
        ('app', 'Mobile App Issue'),
        ('payment', 'Payment System Error'),
        ('account', 'Account Access Problem'),
        ('checkout', 'Checkout Process Issue'),
        ('other', 'Other Technical Issue')
    ],default='website')
    page_url = models.CharField(max_length=255)
    complaint_description = models.TextField(default='')
    issue_image = models.ImageField(upload_to='issue_images/', default='default_issue.png')

    def __str__(self):
        return f"{self.user.email} - {self.page_url}"

class ProductComplaint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=100,choices=[
        ('damaged','Damaged Product'),
        ('defective','Defective/Not Working'),
        ('wrong','Wrong Item Received'),
        ('missing','Missing Parts/Accessories'),
        ('quality','Poor Quality'),
        ('description','Doesn\'t Match Description'),
        ('other','Other Issue')
    ])
    order_number = models.CharField(max_length=100, blank=True)
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to='product_images/', default='default_product.png')
    complaint_description = models.TextField()

    def __str__(self):
        return f"{self.user.email} - {self.product_name}"


