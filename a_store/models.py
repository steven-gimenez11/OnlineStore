from django.db import models
from a_users.models import Profile
import uuid

class Category(models.Model):  # Asegúrate de que este modelo esté definido primero
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

    def get_absolute_url(self):
        return f'/category/{self.slug}'

class Product(models.Model):
    title = models.CharField(max_length=30, null=True)
    image = models.ImageField(upload_to='products/', null=True)
    description = models.TextField(max_length=200, null=True)  # Ampliado a 200 caracteres
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(null=True)
    active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category)  # Relación ManyToMany con Category
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return f'/product/{self.id}'

