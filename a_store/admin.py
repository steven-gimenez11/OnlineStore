from django.contrib import admin
from .models import Product, Category  # Importa todos los modelos que quieras registrar

# Registra el modelo Product
admin.site.register(Product)

# Registra el modelo Category
admin.site.register(Category)
