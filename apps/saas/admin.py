from django.contrib import admin
from .models import Tenant, Domain, SubscriptionPlan, Subscription, SubscriptionPayment


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'contact_email', 'contact_phone', 'is_active', 'created_on')
    list_filter = ('is_active',)
    search_fields = ('name', 'contact_email')


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('domain',)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'max_students', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'plan', 'status', 'start_date', 'end_date', 'auto_renew')
    list_filter = ('status', 'auto_renew')
    search_fields = ('tenant__name',)


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'method', 'source', 'confirmed_by', 'paid_at')
    list_filter = ('method', 'source')
    search_fields = ('transaction_id', 'subscription__tenant__name')