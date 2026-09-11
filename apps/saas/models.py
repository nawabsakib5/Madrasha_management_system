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