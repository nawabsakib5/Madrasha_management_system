from django.db import models
from apps.academics.models import SchoolClass, Section, Subject
from apps.students.models import Student


class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('half_yearly', 'Half Yearly'),
        ('annual', 'Annual'),
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('custom', 'Custom'),
    ]

    name = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.PROTECT, related_name='exams')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.school_class.name}"

    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'
        ordering = ['-start_date']


class ExamSchedule(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.exam.name} - {self.subject.name} - {self.date}"

    class Meta:
        verbose_name = 'Exam Schedule'
        verbose_name_plural = 'Exam Schedules'


class ExamResult(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
        ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.PROTECT, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES, blank=True)
    is_absent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.name} - {self.marks_obtained}"

    class Meta:
        verbose_name = 'Exam Result'
        verbose_name_plural = 'Exam Results'
        unique_together = ('exam', 'student', 'subject')


class AdmitCard(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    roll_no = models.CharField(max_length=20)
    is_issued = models.BooleanField(default=False)
    issued_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.exam.name}"

    class Meta:
        verbose_name = 'Admit Card'
        verbose_name_plural = 'Admit Cards'
        unique_together = ('exam', 'student')