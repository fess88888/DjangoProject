from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product, Contact


def home(request):
    # Выборка последних 5 продуктов по дате создания
    latest_products = Product.objects.order_by('-created_at')[:5]

    # Вывод в консоль (в PyCharm в панели Run или в терминале сервера)
    for p in latest_products:
        print(f"[Home] Товар: {p.product_name}, цена: {p.price}, дата: {p.created_at}")

    return render(request, 'catalog/home.html', {
        'latest_products': latest_products,
    })


def contacts(request):
    contacts_list = Contact.objects.all()
    for c in contacts_list:
        print(f"[Contacts] {c.name}, {c.position}, {c.phone}, {c.email}, {c.address}")
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'catalog/contacts.html', {'contacts': contacts_list, })