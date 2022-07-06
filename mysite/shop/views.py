from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product, SubCategory


def product_list(request, category_slug=None, subcategory_slug=None):
    category = None
    subcategory = None
    subcategories = None
    categories = Category.objects.all()     # вывод всех объектов
    products = Product.objects.filter(available=True)

    if category_slug:       # вывод объектов по категории
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = SubCategory.objects.filter(category=category)
        products = products.filter(subcategory__in=subcategories)

        if subcategory_slug:    # вывод объектов по подкатегории
            subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
            products = products.filter(subcategory=subcategory)

    param = {'category': category, 'categories': categories, 'subcategories': subcategories,
             'subcategory': subcategory, 'products': products}

    return render(request, 'shop/list.html', context=param)


def product_detail(request, product_slug, category_slug, subcategory_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    form = CartAddProductForm()
    return render(request, 'shop/detail.html', {'product': product, 'form': form})
