from django.db import models
from apps.accounts.models import User
from apps.branch.models import Branch, Group


class Guardian(models.Model):
    RELATION_CHOICES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('uncle', 'Uncle'),
        ('aunt', 'Aunt'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(max_length=200)
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    nid_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.relation})"

    class Meta:
        verbose_name = 'Guardian'
        verbose_name_plural = 'Guardians'


class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
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
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)

    # Academic Info
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True)
    roll_no = models.CharField(max_length=20, blank=True)
    admission_date = models.DateField()

    # Guardian
    guardians = models.ManyToManyField(Guardian, related_name='students', blank=True)

    # Documents
    birth_certificate = models.FileField(upload_to='students/documents/', blank=True, null=True)
    previous_certificate = models.FileField(upload_to='students/documents/', blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['student_id']