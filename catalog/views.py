from django.core.exceptions import PermissionDenied
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import ProductForm
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST


def unpublish_product(request, pk):
    if not request.user.has_perm('catalog.can_unpublish_product'):
        raise PermissionDenied
    product = get_object_or_404(Product, pk=pk)
    product.is_published = False
    product.save()
    return redirect('catalog:product_list')


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"


class ContactsView(TemplateView):
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
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")
    login_url = "/users/login/"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")
    login_url = "/users/login/"

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
    login_url = "/users/login/"

    def get_queryset(self):
        user = self.request.user
        # Владелец или модератор (с правом delete_product)
        if user.has_perm('catalog.delete_product'):
            return Product.objects.all()
        return Product.objects.filter(owner=user)
