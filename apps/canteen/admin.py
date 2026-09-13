from django.contrib import admin
from .models import CanteenCategory, CanteenItem, Supplier, Purchase, Sale


@admin.register(CanteenCategory)
class CanteenCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(CanteenItem)
class CanteenItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'phone', 'email')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('item', 'supplier', 'quantity', 'unit_price', 'total_price', 'purchased_at', 'recorded_by')
    list_filter = ('supplier', 'item')
    search_fields = ('item__name', 'supplier__name')
    readonly_fields = ('purchased_at',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'unit_price', 'total_price', 'sold_at', 'sold_by')
    list_filter = ('item',)
    search_fields = ('item__name',)
    readonly_fields = ('sold_at',)