from django.db import models
from django.db.models import SET_NULL


class Category(models.Model):
    category_name = models.CharField(max_length=200, verbose_name='Наименование категории')
    category_description = models.TextField(null=True, blank=True, verbose_name='Описание категории')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['category_name', ]


class Product(models.Model):
    product_name = models.CharField(max_length=200, verbose_name='Наименование продукта')
    product_description = models.TextField(null=True, blank=True, verbose_name='Описание продукта')
    picture = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, null=True, on_delete=SET_NULL, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['product_name',]

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    position = models.CharField(max_length=100, blank=True, verbose_name='Должность')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.TextField(blank=True, verbose_name='Адрес')

    def __str__(self):
        return f"{self.name} ({self.position})"

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
