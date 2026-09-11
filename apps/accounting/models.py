from django.db import models
from apps.accounts.models import User
from apps.students.models import Student
from apps.staff.models import Staff


class FeeCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fee Category'
        verbose_name_plural = 'Fee Categories'


class FeeStructure(models.Model):
    category = models.ForeignKey(FeeCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - ৳{self.amount}"

    class Meta:
        verbose_name = 'Fee Structure'
        verbose_name_plural = 'Fee Structures'


class FeeInvoice(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('void', 'Void'),
    ]

    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='invoices')
    category = models.ForeignKey(FeeCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    month = models.PositiveIntegerField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.category.name} - {self.status}"

    class Meta:
        verbose_name = 'Fee Invoice'
        verbose_name_plural = 'Fee Invoices'


class FeePayment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('bank', 'Bank Transfer'),
    ]

    invoice = models.ForeignKey(FeeInvoice, on_delete=models.PROTECT, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='cash')
    receipt_no = models.CharField(max_length=30, unique=True)
    received_by = models.ForeignKey(User, on_delete=models.PROTECT)
    is_void = models.BooleanField(default=False)
    void_reason = models.TextField(blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receipt_no} - ৳{self.amount_paid}"

    class Meta:
        verbose_name = 'Fee Payment'
        verbose_name_plural = 'Fee Payments'


class CashBookEntry(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    reference = models.CharField(max_length=100, blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.type} - ৳{self.amount}"

    class Meta:
        verbose_name = 'Cash Book Entry'
        verbose_name_plural = 'Cash Book Entries'
        ordering = ['-date']


class SalaryStructure(models.Model):
    SALARY_TYPE_CHOICES = [
        ('govt', 'Government Salary'),
        ('parttime', 'Part-time Salary'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='salary_structures')
    salary_type = models.CharField(max_length=20, choices=SALARY_TYPE_CHOICES, default='govt')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    house_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    effective_from = models.DateField()
    is_active = models.BooleanField(default=True)

    @property
    def total_salary(self):
        return self.basic_salary + self.house_rent + self.transport + self.medical

    def __str__(self):
        return f"{self.staff.full_name} - {self.salary_type} - ৳{self.total_salary}"

    class Meta:
        verbose_name = 'Salary Structure'
        verbose_name_plural = 'Salary Structures'


class SalaryPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('void', 'Void'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='salary_payments')
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.PROTECT)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, default='cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.full_name} - {self.month}/{self.year}"

    class Meta:
        verbose_name = 'Salary Payment'
        verbose_name_plural = 'Salary Payments'
        unique_together = ('staff', 'month', 'year')