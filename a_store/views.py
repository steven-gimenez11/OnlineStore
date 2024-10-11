from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.


def home_view(request):

    products = Product.objects.all()
    
    return render(request, 'home.html', {'products': products})



def product_view(request, pid):

    product = get_object_or_404(Product, id=pid)
    
    return render(request, 'a_products/product_page.html', {'product': product})
