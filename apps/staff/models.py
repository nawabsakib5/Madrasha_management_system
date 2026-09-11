from django.db import models
from apps.accounts.models import User
from apps.branch.models import Branch


class Staff(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    STAFF_TYPE_CHOICES = [
        ('teacher', 'Teacher'),
        ('admin_staff', 'Admin Staff'),
        ('accountant', 'Accountant'),
        ('librarian', 'Librarian'),
        ('guard', 'Guard'),
        ('cleaner', 'Cleaner'),
        ('other', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    # Basic Info
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    staff_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='staff/photos/', blank=True, null=True)
    nid_number = models.CharField(max_length=20, blank=True)

    # Job Info
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    joining_date = models.DateField()
    leaving_date = models.DateField(null=True, blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.staff_id} - {self.full_name}"

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'
        ordering = ['staff_id']


class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    max_days = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Leave Type'
        verbose_name_plural = 'Leave Types'


class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.full_name} - {self.leave_type.name}"

    class Meta:
        verbose_name = 'Leave Application'
        verbose_name_plural = 'Leave Applications'