from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# ─── Role Choices ─────────────────────────────────────────
ROLE_CHOICES = [
    ('super_admin', 'Super Admin'),
    ('admin', 'Admin'),
    ('accountant', 'Accountant'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
    ('parent', 'Parent'),
]


# ─── Custom User Manager ──────────────────────────────────
class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username দিতে হবে')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'super_admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


# ─── Custom User Model ────────────────────────────────────
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # Security fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=True)
    two_factor_enabled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name} ({self.role})"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'