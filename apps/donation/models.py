from django.db import models
from apps.accounts.models import User


class DonationCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Donation Category'
        verbose_name_plural = 'Donation Categories'


class Donor(models.Model):
    DONOR_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization'),
        ('anonymous', 'Anonymous'),
    ]

    name = models.CharField(max_length=200)
    donor_type = models.CharField(max_length=20, choices=DONOR_TYPE_CHOICES, default='individual')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.donor_type})"

    class Meta:
        verbose_name = 'Donor'
        verbose_name_plural = 'Donors'


class Donation(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('bank', 'Bank Transfer'),
        ('online', 'Online'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.PROTECT, related_name='donations')
    category = models.ForeignKey(DonationCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='cash')
    transaction_id = models.CharField(max_length=100, blank=True)
    receipt_no = models.CharField(max_length=30, unique=True)
    note = models.TextField(blank=True)
    received_by = models.ForeignKey(User, on_delete=models.PROTECT)
    donated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.name} - ৳{self.amount}"

    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
        ordering = ['-donated_at']