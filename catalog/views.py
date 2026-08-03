from itertools import product
from lib2to3.fixes.fix_input import context

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from catalog.models import Product, Contact


def products_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/products_list.html', context)


def contacts(request):
    contacts_list = Contact.objects.all()
    for c in contacts_list:
        print(f"[Contacts] {c.name}, {c.position}, {c.phone}, {c.email}, {c.address}")
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'catalog/contacts.html', {'contacts': contacts_list, })


def products_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'catalog/products_detail.html', {'product': product})
