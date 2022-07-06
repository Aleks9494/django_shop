from django.contrib import admin
from .models import Category, Product, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')   # показывать на странице категории в admin
    search_fields = ('name',)         # поиск по имени сверху
    list_filter = ('name',)           # поиск по фильтрам справа
    prepopulated_fields = {'slug': ('name',)}  # заполнение слага автоматически из имени


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # показывать на странице категории в admin
    search_fields = ('name',)  # поиск по имени сверху
    list_filter = ('name',)  # поиск по фильтрам справа
    prepopulated_fields = {'slug': ('name',)}  # заполнение слага автоматически из имени


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'subcategory', 'slug', 'available', 'photo')
    search_fields = ('name',)
    list_filter = ('name', 'available', 'subcategory__name')  # фильтр по именам категорий
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('available', )  # изменение наличия в странице товаров
