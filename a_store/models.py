from django.db import models

# Create your models here.



class Product(models.Model):
    title = models.CharField(max_length=30, null = True)
    description = models.TextField(max_length=50, null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock= models.IntegerField(null=True)
    category = models.ManyToManyField('Category')
    image = models.ImageField(upload_to='products/', null=True)



    def __str__(self):
        return str(self.title)
    


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