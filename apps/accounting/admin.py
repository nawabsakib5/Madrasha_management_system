from django.contrib import admin
from .models import (
    FeeCategory, FeeStructure, FeeInvoice,
    FeePayment, CashBookEntry, SalaryStructure, SalaryPayment
)


@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('category__name',)


@admin.register(FeeInvoice)
class FeeInvoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'category', 'amount', 'due_date', 'month', 'year', 'status')
    list_filter = ('status', 'category', 'year', 'month')
    search_fields = ('student__full_name', 'student__student_id')


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('receipt_no', 'invoice', 'amount_paid', 'method', 'received_by', 'is_void', 'paid_at')
    list_filter = ('method', 'is_void')
    search_fields = ('receipt_no', 'invoice__student__full_name')
    readonly_fields = ('paid_at',)


@admin.register(CashBookEntry)
class CashBookEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'category', 'amount', 'reference', 'recorded_by')
    list_filter = ('type', 'date')
    search_fields = ('category', 'reference', 'description')


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('staff', 'salary_type', 'basic_salary', 'house_rent', 'transport', 'medical', 'effective_from', 'is_active')
    list_filter = ('salary_type', 'is_active')
    search_fields = ('staff__full_name',)


@admin.register(SalaryPayment)
class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ('staff', 'month', 'year', 'amount', 'method', 'status', 'paid_by', 'paid_at')
    list_filter = ('status', 'method', 'year', 'month')
    search_fields = ('staff__full_name',)