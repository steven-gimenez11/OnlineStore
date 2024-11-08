from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from a_store.models import Category
from django.contrib import messages
from a_store.models import Product
from django.http import JsonResponse

# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()


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
    
    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        
        messages.success(request, 'Producto agregado al Carrito')
        response = JsonResponse({'qty': cart_quantity})
        return response

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
