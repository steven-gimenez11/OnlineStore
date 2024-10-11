from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.


def home_view(request):

    products = Product.objects.all()
    
    return render(request, 'home.html', {'products': products})