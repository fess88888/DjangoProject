from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Product


class HomeListView(ListView):
    """Главная страница — список продуктов."""
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"


class ContactsView(TemplateView):
    """Страница контактов."""
    template_name = "catalog/contacts.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # здесь логика обработки формы
        name = request.POST.get("name")
        message = request.POST.get("message")
        # отправка письма, сохранение в БД и т. д.
        return redirect("catalog:contacts")


class ProductDetailView(DetailView):
    """Детальная страница продукта."""
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """Создание продукта."""
    model = Product
    template_name = "catalog/product_form.html"
    fields = ["name", "description", "category", "price", "image"]
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(UpdateView):
    """Редактирование продукта."""
    model = Product
    template_name = "catalog/product_form.html"
    fields = ["name", "description", "category", "price", "image"]
    success_url = reverse_lazy("catalog:home")


class ProductDeleteView(DeleteView):
    """Удаление продукта."""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
