from django.urls import path
from . import views


app_name = 'catalog'

urlpatterns = [
    path('', views.products_list, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('products_detail/<int:product_id>/', views.products_detail, name='products_detail'),
]
