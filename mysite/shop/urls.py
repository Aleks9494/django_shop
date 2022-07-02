from django.urls import path

from .views import *

app_name = 'shop'
urlpatterns = [
    path('', product_list, name='product_list'),
    path('<slug:category_slug>/', product_list, name='product_list_by_category'),
    path('<slug:category_slug>/<slug:product_slug>', product_detail, name='product_detail'),
]

