from django.shortcuts import render, get_object_or_404, redirect
from a_ecart.cart import Cart
from a_store.models import Category
from django.contrib import messages
from a_store.models import Product
from django.http import JsonResponse

# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()  # Productos en el carrito
    quantities = cart.get_quants()  # Cantidades de cada producto
    totals = cart.cart_total()  # Total del carrito

    categories = Category.objects.all()

    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'categories': categories
    }

    return render(request, 'cart_summary.html', context)


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':  # Verificar que la acción sea válida
        try:
            product_id = str(request.POST.get('product_id'))  # Obtener el ID del producto
            product_qty = int(request.POST.get('product_qty'))  # Obtener la cantidad
            product = get_object_or_404(Product, id=product_id)  # Obtener el producto

            cart.add(product=product, quantity=product_qty)  # Agregar al carrito
            cart_quantity = cart.__len__()  # Obtener cantidad total de productos en el carrito

            messages.success(request, 'Producto agregado al carrito')
            return JsonResponse({'qty': cart_quantity})  # Respuesta JSON

        except Exception as e:  # Manejo de errores
            messages.error(request, f'Error al agregar al carrito: {e}')
            return JsonResponse({'error': str(e)}, status=400)

    # Si la acción no es válida o no es POST
    return JsonResponse({'error': 'Método no permitido o acción inválida'}, status=405)


def cart_delete(request):
    cart = Cart(request)
    try:
        if request.POST.get('action') == 'post':
            product_id = str(request.POST.get('product_id'))
            cart.delete(product=product_id)
            response = JsonResponse({'product': product_id})
            messages.warning(request, 'Producto eliminado del carrito')
            return response
    except Exception as e:
        messages.error(request, 'Error al eliminar producto: {}'.format(str(e)))
        return JsonResponse({'error': 'Error al eliminar producto'})

def cart_update(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        
        response = JsonResponse({'qty': product_qty})
        return response
