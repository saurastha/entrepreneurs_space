from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

# Register your models here.

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'shop_name']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['image']


@admin.register(models.ProductFeedback)
class ProductFeedbackAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'rating', 'review', 'timestamp']


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer']


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'city', 'province', 'address_1', 'address_2']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'placed_at', 'id']


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']


@admin.register(models.Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['seller', 'title', 'description']
