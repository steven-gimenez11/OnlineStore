from django.shortcuts import render, get_object_or_404, redirect
from a_ecart.cart import Cart
from a_store.models import Category, Product
from django.contrib import messages
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    product_totals = cart.get_product_totals() 

    total = sum(product_totals.values())

    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'product_totals': product_totals,
        'total': total,
    }

    return render(request, 'cart_summary.html', context)

def cart_add(request):
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        try:
            product_id = str(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            product = get_object_or_404(Product, id=product_id)

            cart.add(product=product, quantity=product_qty)
            cart_quantity = cart.__len__()

            messages.success(request, 'Producto agregado al carrito')
            return JsonResponse({'qty': cart_quantity})

        except Exception as e:
            messages.error(request, f'Error al agregar al carrito: {e}')
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido o acción inválida'}, status=405)

def cart_delete(request):
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        try:
            product_id = str(request.POST.get('product_id'))
            cart.delete(product=product_id)

            cart_quantity = cart.__len__()
            cart_total = cart.cart_total()

            response = JsonResponse({
                'product': product_id,
                'cart_quantity': cart_quantity,
                'cart_total': cart_total
            })
            return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido o acción inválida'}, status=405)

def cart_update(request):
    cart = Cart(request)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        if not product_id or not product_qty:
            return JsonResponse({'error': 'ID de producto o cantidad faltante'}, status=400)

        try:
            product_qty = int(product_qty)
        except ValueError:
            return JsonResponse({'error': 'Cantidad inválida'}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=400)

        cart.update(product, product_qty)

        product_total = cart.get_product_totals().get(str(product_id), 0)
        cart_total = cart.cart_total()

        return JsonResponse({
            'product_total': product_total,
            'cart_total': cart_total
        })

    else:
        return JsonResponse({'error': 'Método de solicitud no permitido'}, status=405)

