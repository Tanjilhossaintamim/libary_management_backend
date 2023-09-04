from django.contrib import admin
from .models import Category, Customer, Book, Order

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ('id', 'name', 'created_at')
    list_per_page = 10


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    '''Admin View for Book'''

    list_display = ('id', 'name', 'category')
    list_per_page = 10


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    '''Admin View for Customer'''

    list_display = ('id', 'user', 'name', 'phone', 'address', 'college')
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''

    list_display = ('id', 'customer', 'book', 'placed_at')
