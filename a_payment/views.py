from django.shortcuts import render, redirect, get_object_or_404
from a_ecart.cart import Cart
from django.contrib import messages
from .forms import ShippingAddressForm, PaymentForm
from django.contrib.auth.models import User
from .models import *
from a_users.models import Profile
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid

# Create your views here.


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = get_object_or_404(Order, id=pk)
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']

            if status == 'true':
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, 'Shipping Status Updated')
            return redirect('home')

        return render(request, 'a_payment/payment_order.html', {'order': order, 'items': items})
    else:
        messages.warning(request, 'Access Denied')
        return redirect('home')


def not_shipped_dash(request):

    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)

            messages.success(request, 'Shipping Status Updated')
            return redirect('home')

        return render(request, 'a_payment/payment_not_shipped_dash.html', {'orders': orders})
    else:
        messages.warning(request, 'Access Denied')
        return redirect('home')


def shipped_dash(request):

    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)

            now = datetime.datetime.now()
            order.update(shipped=False)

            messages.success(request, 'Shipping Status Updated')
            return redirect('home')

        return render(request, 'a_payment/payment_shipped_dash.html', {'orders': orders})
    else:
        messages.warning(request, 'Access Denied')
        return redirect('home')


def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        # Create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items

            # Get the order ID
            order_id = create_order.pk

            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                price = product.price

                # Get quantity
                for key, value in quantities().items():
                    if key == product.id:
                        # Create order item
                        create_order_item = OrderItem(
                            order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            # Delete Cart from Database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database (old_cart field)
            current_user.update(old_cart="")

            messages.success(request, "Order Placed!")
            return redirect('home')

        else:
            # not logged in
            # Create Order
            create_order = Order(full_name=full_name, email=email,
                                 shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items

            # Get the order ID
            order_id = create_order.pk

            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price

                price = product.price

                # Get quantity
                for key, value in quantities().items():
                    if key == product.id:
                        # Create order item
                        create_order_item = OrderItem(
                            order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            messages.success(request, "Order Placed!")
            return redirect('home')

    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def billing_info(request):

    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        form = request.POST

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        
        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        host = request.get_host()
        
        my_Invoice = str(uuid.uuid4())
        
        # Create Paypal Form
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': totals,
            'item_name': 'Sneaker Order',
            'no_shipping': '2',
            'invoice': my_Invoice,
            'currency_code': 'USD', # EUR for Euros
            'notify_url': 'https://{}{}'.format(host, reverse("paypal-ipn")),
            'return_url': 'https://{}{}'.format(host, reverse("payment-success")),
            'cancel_return': 'https://{}{}'.format(host, reverse("payment-failed")),
        }
        
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid, invoice=my_Invoice)
            create_order.save()

            # Add order items

            # Get the order ID
            order_id = create_order.pk

            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                price = product.price

                # Get quantity
                for key, value in quantities().items():
                    if key == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()


            # Delete Cart from Database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database (old_cart field)
            current_user.update(old_cart="")

            return render(request, 'a_payment/payment_billing_info.html', {'cart_products': cart_products,
                                                                           'quantities': quantities,
                                                                           'totals': totals,
                                                                           'form': request.POST,
                                                                           'billing_form': billing_form,
                                                                           'paypal_form': paypal_form
                                                                           })

        else:
            # not logged in
            # Create Order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid, invoice=my_Invoice)
            create_order.save()

            # Add order items

            # Get the order ID
            order_id = create_order.pk

            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price

                price = product.price

                # Get quantity
                for key, value in quantities().items():
                    if key == product.id:
                        # Create order item
                        create_order_item = OrderItem(
                            order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()


            billing_form = PaymentForm()
            return render(request, 'a_payment/payment_billing_info.html', {'cart_products': cart_products,
                                                                            'quantities': quantities,
                                                                            'totals': totals,
                                                                            'form': request.POST,
                                                                            'billing_form': billing_form, 
                                                                            'paypal_form': paypal_form })
            
    else:
        messages.info(request, 'Acceco Denegado')
        return redirect('home')


def checkout(request):

    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:

        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = ShippingAddressForm(
            request.POST or None, instance=shipping_user)
        return render(request, 'a_payment/payment_checkout.html', {'cart_products': cart_products,
                                                                   'quantities': quantities,
                                                                   'totals': totals,
                                                                   'form': form, })
    else:
        form = ShippingAddressForm(request.POST or None)
        return render(request, 'a_payment/payment_checkout.html', {'cart_products': cart_products,
                                                                   'quantities': quantities,
                                                                   'totals': totals,
                                                                   'form': form, })


def payment_success(request):
    
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    # Delete our cart
    for key in list(request.session.keys()):
        if key == "session_key":
            # Delete the key
            del request.session[key]
    
    return render(request, 'a_payment/payment_success.html')


def payment_failed(request):
    return render(request, 'a_payment/payment_failed.html')
    