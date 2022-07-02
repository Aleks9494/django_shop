from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    param = {'category': category, 'categories': categories, 'products': products}

    return render(request, 'shop/list.html', context=param)


def product_detail(request, product_slug, category_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    form = CartAddProductForm()
    return render(request, 'shop/detail.html', {'product': product, 'form': form})
