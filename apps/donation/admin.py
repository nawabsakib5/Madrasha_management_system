from django.contrib import admin
from .models import DonationCategory, Donor, Donation


@admin.register(DonationCategory)
class DonationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'donor_type', 'phone', 'email', 'is_active')
    list_filter = ('donor_type', 'is_active')
    search_fields = ('name', 'phone', 'email')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'category', 'amount', 'method', 'receipt_no', 'received_by', 'donated_at')
    list_filter = ('method', 'category')
    search_fields = ('donor__name', 'receipt_no', 'transaction_id')
    readonly_fields = ('donated_at',)