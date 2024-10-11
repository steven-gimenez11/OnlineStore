from django.db import models
from a_users.models import Profile
import uuid

# Create your models here.



class Product(models.Model):
    title = models.CharField(max_length=30, null = True)
    image = models.ImageField(upload_to='products/', null=True)
    description = models.TextField(max_length=50, null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock= models.IntegerField(null=True)
    active = models.BooleanField(default=True)
    category = models.ManyToManyField('Category')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key = True, editable = False)



    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-created']
    
    def get_absolute_url(self):
        return f'/product/{self.id}'
    


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        
    def get_absolute_url(self):
        return f'/category/{self.slug}'




class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='',  blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status =models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.product