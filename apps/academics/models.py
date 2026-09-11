from django.db import models
from apps.branch.models import Branch, Group


class SchoolClass(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='classes')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.branch.name} - {self.name}"

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        ordering = ['order']
        unique_together = ('branch', 'code')


class Section(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(default=40)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.school_class.name} - {self.name}"

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        unique_together = ('school_class', 'name')


class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='subjects')
    full_marks = models.PositiveIntegerField(default=100)
    pass_marks = models.PositiveIntegerField(default=33)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.school_class.name} - {self.name}"

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        unique_together = ('school_class', 'code')


class ClassRoutine(models.Model):
    DAY_CHOICES = [
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
    ]

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='routines')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.section} - {self.subject.name} ({self.day})"

    class Meta:
        verbose_name = 'Class Routine'
        verbose_name_plural = 'Class Routines'