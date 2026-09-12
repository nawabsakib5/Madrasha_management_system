from django.db import models
from apps.students.models import Student
from apps.staff.models import Staff
from apps.academics.models import Section


class StudentAttendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('leave', 'Leave'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.status}"

    class Meta:
        verbose_name = 'Student Attendance'
        verbose_name_plural = 'Student Attendances'
        unique_together = ('student', 'date')
        ordering = ['-date']


class StaffAttendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('leave', 'Leave'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.full_name} - {self.date} - {self.status}"

    class Meta:
        verbose_name = 'Staff Attendance'
        verbose_name_plural = 'Staff Attendances'
        unique_together = ('staff', 'date')
        ordering = ['-date']