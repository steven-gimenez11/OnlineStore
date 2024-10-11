from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('product/<pid>/', product_view, name='product-detail'),
]
