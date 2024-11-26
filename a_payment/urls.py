from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment/', views.payment_page, name='payment'),
    path('confirmation/', views.payment_confirmation, name='confirmation'),
]
