from django.contrib import admin
from .models import Product, Category, Order  # Importa todos los modelos que quieras registrar

# Registra el modelo Product
admin.site.register(Product)

# Registra el modelo Category
admin.site.register(Category)

# Registra el modelo Order si lo necesitas
admin.site.register(Order)
