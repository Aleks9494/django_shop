from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'  # название в админ-панели
        verbose_name_plural = 'Категории'  # для множественного числа
        ordering = ['name']   # сортировка по имени в админ-панели

    # формирование ссылок с переменными адресами согласно правилу в urls.py
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', kwargs={'category_slug': self.slug})


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories',
                                    on_delete=models.CASCADE, verbose_name='Категории')
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'  # название в админ-панели
        verbose_name_plural = 'Подкатегории'  # для множественного числа
        ordering = ['name']  # сортировка по имени в админ-панели

    # формирование ссылок с переменными адресами согласно правилу в urls.py
    def get_absolute_url(self):
        return reverse('shop:product_list_by_subcategory', kwargs={'subcategory_slug': self.slug,
                                                                   'category_slug': self.category.slug})


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, related_name='products',
                                 on_delete=models.CASCADE, verbose_name='Подкатегории')

    name = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    photo = models.ImageField(upload_to="product/%Y/%m/%d/", blank=True, verbose_name='Фото')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='Наличие')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'product_slug': self.slug,
                                                      'subcategory_slug': self.subcategory.slug,
                                                      'category_slug': self.subcategory.category.slug})
