from django.shortcuts import render, get_object_or_404, redirect  # Importa las funciones necesarias para manejar las vistas
from .models import *  # Importa todos los modelos (en este caso, el modelo Product)
from django.contrib.auth.decorators import user_passes_test  # Importa el decorador para verificar permisos de usuario
from .forms import * 

# Vista principal que muestra todos los productos
def home_view(request):
    products = Product.objects.all()  # Obtiene todos los productos de la base de datos
    return render(request, 'home.html', {'products': products})  # Renderiza la plantilla 'home.html' pasando la lista de productos

# Vista que muestra los detalles de un producto específico
def product_view(request, pid):
    product = get_object_or_404(Product, id=pid)
    return render(request, 'a_products/product_page.html', {'product': product})

# Vista que permite editar un producto existente
def product_edit(request, pid):
    product = get_object_or_404(Product, id=pid)  # Obtiene el producto por su ID
    if request.method == 'POST':  # Verifica si el método de la solicitud es POST (envío de formulario)
        form = ProductEditForm(request.POST, request.FILES, instance=product)  # Usa ProductEditForm aquí
        if form.is_valid():  # Verifica si el formulario es válido
            form.save()  # Guarda los cambios del producto en la base de datos
            return redirect('product-detail', pid=product.id)  # Redirige a la vista de detalles del producto editado
    else:
        form = ProductEditForm(instance=product)  # Si no es POST, crea el formulario precargado con los datos del producto
    
    return render(request, 'a_products/product_edit.html', {'form': form})  # Renderiza la plantilla del formulario pasando el formulario

# Función para verificar si un usuario es administrador
def is_admin(user):
    return user.is_superuser  # Devuelve True si el usuario es un superusuario

@user_passes_test(is_admin)  # Esto asegura que solo los administradores accedan
def product_delete(request, pid):
    product = get_object_or_404(Product, id=pid)  # Obtiene el producto por su ID
    product.delete()  # Elimina el producto de la base de datos
    return redirect('home')  # Redirige a la página principal después de eliminar el producto

# Vista para crear un nuevo producto
def product_create(request):
    if request.method == 'POST':  # Verifica si el método de la solicitud es POST (envío de formulario)
        form = ProductCreateForm(request.POST, request.FILES)  # Crea un formulario con los datos del nuevo producto
        if form.is_valid():  # Verifica si el formulario es válido
            form.save()  # Guarda el nuevo producto en la base de datos
            return redirect('home')  # Redirige a la página principal
    else:
        form = ProductCreateForm()  # Si no es POST, crea un formulario vacío para el nuevo producto

    return render(request, 'a_products/product_create.html', {'form': form})  # Renderiza la plantilla del formulario pasando el formulario
