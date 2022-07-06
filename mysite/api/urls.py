from django.urls import path

from .views import *

app_name = 'api'

urlpatterns = [
    path('product_list', ProductsApiView.as_view(), name='product_list_api'),
    path('product_list/<int:cat_id>', CatApiView.as_view(), name='product_list_by_cat_api'),
    path('product_list/<int:cat_id>/<int:subcat_id>', SubCatApiView.as_view(), name='product_list_by_subcat_api'),
    path('product_list/<int:cat_id>/<int:subcat_id>/<int:pr_id>', ProductApiView.as_view(), name='product_api'),
    path('cart', CartApiView.as_view(), name='cart'),
    path('cart/add', AddOrderToCart.as_view(), name='cart_add'),
    path('product_list/<int:cat_id>/<int:subcat_id>/<int:pr_id>/add', ProductAddApiView.as_view(),
         name='product_add_api'),
    path('product_list/<int:cat_id>/<int:subcat_id>/<int:pr_id>/del', ProductDelApiView.as_view(),
         name='product_del_api'),
]
