from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'


class Department(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.branch.name} - {self.name}"

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        unique_together = ('branch', 'code')


class Group(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='groups')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='groups', null=True, blank=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField(default=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.branch.name} - {self.name}"

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        unique_together = ('branch', 'code')