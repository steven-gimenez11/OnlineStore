from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserPayment
from .forms import PaymentForm 
from a_ecart.cart import Cart
from django.contrib import messages

@login_required
def payment_page(request):
    cart = Cart(request)

    if len(cart) == 0:  
        messages.error(request, "Tu carrito está vacío.")
        return redirect('a_store:home')  

    products = cart.get_products() 
    total = cart.cart_total() 

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            user_payment = UserPayment(
                user=request.user,
                stripe_customer="fake_customer_id", 
                stripe_checkout_id="fake_checkout_id", 
                stripe_product_id = "fake_product_id", 
                product_name="Demo Product", 
                price=total,  
                currency="USD",
                quantity=len(cart),  
                has_paid=False 
            )
            user_payment.save()

            cart.clear()

            messages.success(request, 'Compra realizada con éxito.')
            return redirect('payment:confirmation')  
    else:
        form = PaymentForm() 

    return render(request, 'payment_form.html', {
        'cart': cart, 
        'products': products, 
        'total': total,
        'form': form  
    })


@login_required
def payment_confirmation(request):
    return render(request, 'payment_confirmation.html')
