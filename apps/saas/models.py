from django_tenants.models import TenantMixin, DomainMixin
from django.db import models


class Tenant(TenantMixin):
    """
    প্রতিটা Madrasa একটা Tenant
    একটা Tenant = একটা আলাদা PostgreSQL schema
    """
    name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    # django-tenants এর জন্য required
    auto_create_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    """
    প্রতিটা Tenant এর subdomain
    example: darul-ulum.yoursaas.com
    """
    pass


# ─── Subscription Plan ────────────────────────────────────
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=365)
    max_students = models.PositiveIntegerField(null=True, blank=True)
    features = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ৳{self.price}"

    class Meta:
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'


# ─── Subscription ─────────────────────────────────────────
class Subscription(models.Model):
    STATUS_CHOICES = [
        ('trial', 'Trial'),
        ('active', 'Active'),
        ('grace', 'Grace Period'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trial')
    auto_renew = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.status}"

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'


# ─── Subscription Payment ─────────────────────────────────
class SubscriptionPayment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('bank', 'Bank Transfer'),
    ]

    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)
    source = models.CharField(max_length=20, choices=[('manual', 'Manual'), ('gateway', 'Gateway')], default='manual')
    confirmed_by = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscription.tenant.name} - ৳{self.amount}"

    class Meta:
        verbose_name = 'Subscription Payment'
        verbose_name_plural = 'Subscription Payments'