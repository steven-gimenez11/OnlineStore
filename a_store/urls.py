from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),  # Página principal
    path('category/<category>/', home_view, name='category'),
    path('product/<uuid:pid>/', product_view, name='product-detail'),  # Detalle del producto con UUID
    path('product/<uuid:pid>/delete/', product_delete, name='product-delete'),  # Eliminar producto
    path('product/<uuid:pid>/edit/', product_edit, name='product-edit'),  # Editar producto
    path('product/create/', product_create, name='product-create'),  # Crear producto
]
