from django.db import models
from apps.students.models import Student
from apps.staff.models import Staff


class BookCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Book Category'
        verbose_name_plural = 'Book Categories'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    isbn = models.CharField(max_length=20, blank=True, unique=True)
    category = models.ForeignKey(BookCategory, on_delete=models.PROTECT)
    publisher = models.CharField(max_length=200, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class BookIssue(models.Model):
    STATUS_CHOICES = [
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    BORROWER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
    ]

    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='issues')
    borrower_type = models.CharField(max_length=10, choices=BORROWER_TYPE_CHOICES)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, null=True, blank=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        borrower = self.student or self.staff
        return f"{self.book.title} - {borrower}"

    class Meta:
        verbose_name = 'Book Issue'
        verbose_name_plural = 'Book Issues'
        ordering = ['-issue_date']